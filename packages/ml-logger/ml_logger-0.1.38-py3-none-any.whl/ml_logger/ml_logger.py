from io import BytesIO

import os
from datetime import datetime

from typing import Union, Callable, Any
from collections import OrderedDict, deque, Sequence
from numbers import Number
from itertools import zip_longest

from ml_logger.full_duplex import Duplex
from ml_logger.log_client import LogClient
from termcolor import colored as c
import numpy as np


class Stream:
    def __init__(self, len=100):
        self.d = deque(maxlen=len)

    def append(self, d):
        self.d.append(d)

    @property
    def latest(self):
        return self.d[-1]

    @property
    def mean(self):
        try:
            return np.mean(self.d)
        except ValueError:
            return None

    @property
    def max(self):
        try:
            return np.max(self.d)
        except ValueError:
            return None

    @property
    def min(self):
        try:
            return np.min(self.d)
        except ValueError:
            return None


class Color:
    # noinspection PyInitNewSignature
    def __init__(self, value, color=None, formatter: Union[Callable[[Any], Any], None] = lambda v: v):
        self.value = value
        self.color = color
        self.formatter = formatter

    def __str__(self):
        return str(self.formatter(self.value)) if callable(self.formatter) else str(self.value)

    def __len__(self):
        return len(str(self.value))

    def __format__(self, format_spec):
        if self.color in [None, 'default']:
            return self.formatter(self.value).__format__(format_spec)
        else:
            return c(self.formatter(self.value).__format__(format_spec), self.color)


def percent(v):
    return '{:.02%}'.format(round(v * 100))


def ms(v):
    return '{:.1f}ms'.format(v * 1000)


def sec(v):
    return '{:.3f}s'.format(v)


def default(value, *args, **kwargs):
    return Color(value, 'default', *args, **kwargs)


def red(value, *args, **kwargs):
    return Color(value, 'red', *args, **kwargs)


def green(value, *args, **kwargs):
    return Color(value, 'green', *args, **kwargs)


def gray(value, *args, **kwargs):
    return Color(value, 'gray', *args, **kwargs)


def grey(value, *args, **kwargs):
    return Color(value, 'gray', *args, **kwargs)


def yellow(value, *args, **kwargs):
    return Color(value, 'yellow', *args, **kwargs)


def brown(value, *args, **kwargs):
    return Color(value, 'brown', *args, **kwargs)


def metrify(data):
    """Help convert non-json serializable objects, such as

    :param data:
    :return:
    """
    if hasattr(data, 'shape') and len(data.shape) > 0:
        return list(data)
    elif isinstance(data, Sequence):
        return data
    elif isinstance(data, Number):
        return data
    elif data is None:
        return data
    elif type(data) in [dict, str, bool, str]:
        return data
    # todo: add datetime support
    elif not hasattr(data, 'dtype'):
        return str(data)
    elif str(data.dtype).startswith('int'):
        return int(data)
    elif str(data.dtype).startswith('float'):
        return float(data)
    else:
        return str(data)


class ML_Logger:
    logger = None
    log_directory = None

    def split(self):
        """
        returns a datetime object. You can get integer seconds and miliseconds (both int) from it.
        Note: This is Not idempotent, which is why it is not a property.

        :return: float (seconds/miliseconds)
        """
        new_tic = self.now
        try:
            dt = new_tic - self._tic
            self._tic = new_tic
            return dt.total_seconds()
        except AttributeError:
            self._tic = new_tic
            return None

    @property
    def now(self, fmt=None):
        from datetime import datetime
        now = datetime.now()
        return now.strftime(fmt) if fmt else now

    def diff(self, diff_directory=".", diff_filename="index.diff", silent=False):
        """
        example usage: M.diff('.')
        :param diff_directory: The root directory to call `git diff`.
        :param log_directory: The overriding log directory to save this diff index file
        :param diff_filename: The filename for the diff file.
        :return: None
        """
        import subprocess
        try:
            cmd = f'cd "{os.path.realpath(diff_directory)}" && git add . && git --no-pager diff HEAD'
            if not silent: self.print(cmd)
            p = subprocess.check_output(cmd, shell=True)  # Save git diff to experiment directory
            self.log_text(p.decode('utf-8').strip(), diff_filename, silent=silent)
        except subprocess.CalledProcessError as e:
            self.print("not storing the git diff due to {}".format(e))

    @property
    def __current_branch__(self):
        import subprocess
        try:
            cmd = f'git symbolic-ref HEAD'
            p = subprocess.check_output(cmd, shell=True)  # Save git diff to experiment directory
            return p.decode('utf-8').strip()
        except subprocess.CalledProcessError:
            return None

    @property
    def __head__(self):
        """returns the git revision hash of the head if inside a git repository"""
        return self.git_rev('HEAD')

    def git_rev(self, branch):
        """
        returns the git revision hash of the branch that you pass in.
        full reference here: https://stackoverflow.com/a/949391
        the `show-ref` and the `for-each-ref` commands both show a list of refs. We only need to get the
        ref hash for the revision, not the entire branch of by tag.
        """
        import subprocess
        try:
            cmd = ['git', 'rev-parse', branch]
            p = subprocess.check_output(cmd)  # Save git diff to experiment directory
            return p.decode('utf-8').strip()
        except subprocess.CalledProcessError:
            return None

    @property
    def __tags__(self):
        return self.git_tags()

    def git_tags(self):
        import subprocess
        try:
            cmd = ["git", "describe", "--tags"]
            p = subprocess.check_output(cmd)  # Save git diff to experiment directory
            return p.decode('utf-8').strip()
        except subprocess.CalledProcessError:
            return None

    def diff_file(self, path, silent=False):
        raise NotImplemented

    @property
    def hostname(self):
        import subprocess
        cmd = 'hostname -f'
        try:
            p = subprocess.check_output(cmd, shell=True)  # Save git diff to experiment directory
            return p.decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            self.print(f"can not get obtain hostname via `{cmd}` due to exception: {e}")
            return None

    # noinspection PyInitNewSignature
    def __init__(self, log_directory: str = None, prefix="", buffer_size=2048, max_workers=5):
        """
        :param log_directory: Overloaded to use either
            - file://some_abs_dir
            - http://19.2.34.3:8081
            - /tmp/some_dir
        :param prefix: The directory relative to those above
            - prefix: causal_infogan => /tmp/some_dir/causal_infogan
            - prefix: "" => /tmp/some_dir
        """
        # self.summary_writer = tf.summary.FileWriter(log_directory)
        self.step = None
        self.duplex = None
        self.timestamp = None
        self.data = OrderedDict()
        self.flush()
        self.print_buffer_size = buffer_size
        self.do_not_print_list = set()
        assert not os.path.isabs(prefix), "prefix can not start with `/`"
        self.prefix = prefix

        # todo: add https support
        if log_directory:
            self.logger = LogClient(url=log_directory, max_workers=max_workers)
            self.log_directory = log_directory

    configure = __init__

    def ping(self, status='running', interval=None):
        """
        pings the instrumentation server to stay alive. Gets a control signal in return.
        The background thread is responsible for making the call . This method just returns the buffered
        signal synchronously.

        :return: tuple signals
        """
        if not self.duplex:
            def thunk(*statuses):
                nonlocal self
                if len(statuses) > 0:
                    return self.logger.ping(self.prefix, statuses[-1])
                else:
                    return self.logger.ping(self.prefix, "running")

            self.duplex = Duplex(thunk, interval or 120)  # default interval is two minutes
            self.duplex.start()
        if interval:
            self.duplex.keep_alive_interval = interval

        buffer = self.duplex.read_buffer()
        self.duplex.send(status)
        return buffer

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self.summary_writer.close()
        # todo: wait for logger to finish upload in async mode.
        self.flush()

    def remove(self, path):
        """
        removes by path

        :param path:
        :return:
        """
        abs_path = os.path.join(self.prefix, path)
        self.logger._delete(abs_path)

    def log_params(self, path="parameters.pkl", **kwargs):
        key_width = 30
        value_width = 20

        _kwargs = {}
        table = []
        for n, (title, section_data) in enumerate(kwargs.items()):
            table.append('═' * (key_width) + ('═' if n == 0 else '╧') + '═' * (value_width))
            table.append(c('{:^{}}'.format(title, key_width), 'yellow') + "")
            table.append('─' * (key_width) + "┬" + '─' * (value_width))
            if not hasattr(section_data, 'items'):
                table.append(section_data)
                _kwargs[title] = metrify(section_data)
            else:
                _param_dict = {}
                for key, value in section_data.items():
                    _param_dict[key] = metrify(value.v if type(value) is Color else value)
                    value_string = str(value)
                    table.append('{:^{}}'.format(key, key_width) + "│" + '{:<{}}'.format(value_string, value_width))
                _kwargs[title] = _param_dict

        if "n" in locals():
            table.append('═' * (key_width) + ('═' if n == 0 else '╧') + '═' * (value_width))

        # todo: add logging hook
        # todo: add yml support
        self.print('\n'.join(table))
        self.log_data(path=path, data=_kwargs)

    def log_data(self, data, path=None, overwrite=False):
        """
        Append data to the file located at the path specified.

        :param data: python data object to be saved
        :param path: path for the object, relative to the root logging directory.
        :param overwrite: boolean flag to switch between 'appending' mode and 'overwrite' mode.
        :return: None
        """
        path = path or "data.pkl"
        abs_path = os.path.join(self.prefix or "", path)
        if overwrite:
            self.logger.log(key=abs_path, data=data, overwrite=overwrite)
        else:
            self.logger.log(key=abs_path, data=data)

    def log_keyvalue(self, key: str, value: Any, step: Union[int, Color] = None, silent=False) -> None:
        if self.step != step and step is not None:
            self.flush()
            self.step = step

        self.timestamp = np.datetime64(datetime.now())

        if silent:
            self.do_not_print_list.update([key])

        if step is None and self.step is None and key in self.data:
            self.flush()

        if key in self.data:
            if type(self.data) is list:
                self.data[key].append(value.value if type(value) is Color else value)
            else:
                self.data[key] = [self.data[key]] + [value.value if type(value) is Color else value]
        else:
            self.data[key] = value.value if type(value) is Color else value

    def log(self, *dicts, step: Union[int, Color] = None, silent=False, **kwargs) -> None:
        """
        log dictionaries of data, key=value pairs at step == step.

        :param step: the global step, be it the global timesteps or the epoch step
        :param dicts: a dictionary or a list of dictionaries of key/value pairs, allowing more flexible key name with '/' etc.
        :param silent: Bool, log but do not print. To keep the standard out silent.
        :param kwargs: key/value arguments.
        :return:
        """
        if self.step != step and step is not None:
            self.flush()
            self.step = step

        self.timestamp = np.datetime64(datetime.now())

        data_dict = {}
        for d in dicts:
            data_dict.update(d)
        data_dict.update(kwargs)

        if silent:
            self.do_not_print_list.update(data_dict.keys())

        # todo: add logging hook
        for key, v in data_dict.items():
            if key in self.data:
                if type(self.data) is list:
                    self.data[key].append(_v)
                else:
                    self.data[key] = [self.data[key], v.value if type(v) is Color else v]
            else:
                self.data[key] = v.value if type(v) is Color else v

    @staticmethod
    def _tabular(data, fmt=".3f", do_not_print_list=tuple(), min_key_width=20, min_value_width=20):
        keys = [k for k in data.keys() if k not in do_not_print_list]
        if len(keys) > 0:
            max_key_len = max([min_key_width] + [len(k) for k in keys])
            max_value_len = max([min_value_width] + [len(str(data[k])) for k in keys])
            output = None
            for k in keys:
                v = f"{data[k]:{fmt}}"
                if output is None:
                    output = "╒" + "═" * max_key_len + "╤" + "═" * max_value_len + "╕\n"
                else:
                    output += "├" + "─" * max_key_len + "┼" + "─" * max_value_len + "┤\n"
                if k not in do_not_print_list:
                    k = k.replace('_', " ")
                    v = "NA" if v is None else v  # for NoneTypes which doesn't have __format__ method
                    output += f"│{k:^{max_key_len}}│{v:^{max_value_len}}│\n"
            output += "╘" + "═" * max_key_len + "╧" + "═" * max_value_len + "╛\n"
            return output

    @staticmethod
    def _row_table(data, fmt=".3f", do_not_print_list=tuple(), min_column_width=5):
        """applies to metrics keys with multiple values"""
        keys = [k for k in data.keys() if k not in do_not_print_list]
        output = ""
        if len(keys) > 0:
            values = [values if type(values) is list else [values] for values in data.values()]
            max_key_width = max([min_column_width] + [len(k) for k in keys])
            max_value_len = max([min_column_width] + [len(f"{v:{fmt}}") for d in values for v in d])
            max_width = max(max_key_width, max_value_len)
            output += '|'.join([f"{key.replace('-', ' '):^{max_width}}" for key in keys]) + "\n"
            output += "┼".join(["─" * max_width] * len(keys)) + "\n"
            for row in zip_longest(*values):
                output += '|'.join([f"{value:^{max_width}{fmt}}" for value in row]) + "\n"
            return output

    def flush(self, file_name="metrics.pkl", fmt=".3f"):
        if self.data:
            try:
                output = self._tabular(self.data, fmt, self.do_not_print_list)
            except Exception as e:
                output = self._row_table(self.data, fmt, self.do_not_print_list)
            self.print(output)
            self.logger.log(key=os.path.join(self.prefix or "", file_name or "metrics.pkl"),
                            data=dict(_step=self.step, _timestamp=str(self.timestamp), **self.data))
            self.data.clear()
            self.do_not_print_list.clear()

        self.print_flush()

    def log_file(self, file_path, namespace='files', silent=True):
        # todo: make it possible to log multiple files
        # todo: log dir
        from pathlib import Path
        content = Path(file_path).read_text()
        basename = os.path.basename(file_path)
        self.log_text(content, filename=os.path.join(namespace, basename), silent=silent)

    def log_dir(self, dir_path, namespace='', excludes=tuple(), silent=True):
        """log a directory"""

    def log_images(self, key, stack, ncol=5, nrows=2, namespace="image", fstring="{:04d}.png"):
        """note: might makesense to push the operation to the server instead.
        logs a stack of images from a tensor object. Could also be part of the server code.

        update: client-side makes more sense, less data to send.
        """
        pass

    def log_image(self, image, key, namespace="images", format="png"):
        """
        DONE: IMPROVE API. I'm not a big fan of this particular api.
        Logs an image via the summary writer.
        TODO: add support for PIL images etc.
        reference: https://gist.github.com/gyglim/1f8dfb1b5c82627ae3efcfbbadb9f514

        Because the image keys are passed in as variable keys, it is not as easy to use a string literal
        for the file name (key). as a result, we generate the numerated filename for the user.

        value: numpy object Size(w, h, 3)

        """
        if format:
            key += "." + format

        filename = os.path.join(self.prefix or "", namespace, key)
        self.logger.send_image(key=filename, data=image)

    def log_video(self, frame_stack, key, namespace='videos', format=None, fps=20, macro_block_size=None,
                  **imageio_kwargs):
        """
        Let's do the compression here. Video frames are first written to a temporary file
        and the file containing the compressed data is sent over as a file buffer.
        
        Save a stack of images to

        :param frame_stack:
        :param key:
        :param namespace:
        :param fmt:
        :param ext:
        :param step:
        :param imageio_kwargs:
        :return:
        """
        if format:
            key += "." + format
        else:
            # noinspection PyShadowingBuiltins
            _, format = os.path.splitext(key)
            if format:
                # noinspection PyShadowingBuiltins
                format = format[1:]  # to remove the dot
            else:
                # noinspection PyShadowingBuiltins
                format = "mp4"
                key += "." + format

        filename = os.path.join(self.prefix or "", namespace, key)

        import tempfile, imageio
        with tempfile.NamedTemporaryFile(suffix=f'.{format}') as ntp:
            try:
                imageio.mimsave(ntp.name, frame_stack, format=format, fps=fps, **imageio_kwargs)
            except imageio.core.NeedDownloadError:
                imageio.plugins.ffmpeg.download()
                imageio.mimsave(ntp.name, frame_stack, format=format, fps=fps, **imageio_kwargs)
            ntp.seek(0)
            self.logger.log_buffer(key=filename, buf=ntp.read())

    def log_pyplot(self, key="plot", fig=None, format=None, namespace="plots", **kwargs):
        """
        does not handle pdf and svg file formats. A big annoying.

        ref: see this link https://stackoverflow.com/a/8598881/1560241

        :param key:
        :param fig:
        :param namespace:
        :param fmt:
        :param step:
        :return:
        """
        # can not simplify the logic, because we can't pass the filename to pyplot. A buffer is passed in instead.
        if format:  # so allow key with dots in it: metric_plot.text.plot + ".png". Because user intention is clear
            key += "." + format
        else:
            _, format = os.path.splitext(key)
            if format:
                format = format[1:]  # to get rid of the "." at the begining of '.svg'.
            else:
                format = "png"
                key += "." + format

        if fig is None:
            from matplotlib import pyplot as plt
            fig = plt.gcf()

        buf = BytesIO()
        fig.savefig(buf, format=format, **kwargs)
        buf.seek(0)

        path = os.path.join(self.prefix or "", namespace, key)
        self.logger.log_buffer(path, buf.read())
        return key

    def savefig(self, key, fig=None, format=None, **kwargs):
        """
        This one overrides the namespace default of log_pyplot.
        This way, the key behave exactly the same way pyplot.savefig behaves.

        default plotting file name is plot.png under the current directory


        """
        self.log_pyplot(key=key, fig=fig, format=format, namespace="", **kwargs)

    def log_module(self, namespace="modules", fmt="04d", step=None, **kwargs):
        """
        log torch module

        todo: log tensorflow modules.

        :param fmt: 03d, 0.2f etc. The formatting string for the step key.
        :param step:
        :param namespace:
        :param kwargs:
        :return:
        """
        if self.step != step and step is not None:
            self.flush()
            self.step = step

        for var_name, module in kwargs.items():
            # todo: this is torch-specific code. figure out a better way.
            ps = {k: v.cpu().detach().numpy() for k, v in module.state_dict().items()}
            # we use the number first file names to help organize modules by epoch.
            path = os.path.join(namespace, f'{var_name}.pkl' if self.step is None else f'{step:{fmt}}_{var_name}.pkl')
            self.log_data(path=path, data=ps)

    def save_variables(self, variables, path=None, namespace="checkpoints", keys=None):
        """
        save tensorflow variables in a dictionary

        :param variables:
        :param path:
        :param namespace:
        :param keys:
        :return:
        """
        import os
        if keys is None:
            keys = [v.name for v in variables]
        assert len(keys) == len(variables), 'the keys and the variables have to be the same length.'
        if path is None:
            path = "variables.pkl"
        import tensorflow as tf
        sess = tf.get_default_session()
        vals = sess.run(variables)
        weight_dict = {k.split(":")[0]: v for k, v in zip(keys, vals)}
        logger.log_data(weight_dict, os.path.join(namespace, path))

    def load_variables(self, path):
        """
        load the saved value from a pickle file, into a tensorflow variable.
        :param path:
        :return:
        """
        import tensorflow as tf
        weight_dict, = logger.load_pkl(path)
        sess = tf.get_default_session()
        all_variables = {v.name.split(":")[0]: v
                         for v in tf.global_variables()
                         if v.name.split(":")[0] in weight_dict}
        for name, val in weight_dict.items():
            var = all_variables[name]
            var.load(val, sess)

    def load_file(self, key):
        """ return the binary stream, most versatile.

        :param key:
        :return:
        """
        return self.logger.read(os.path.join(self.prefix, key))

    def load_pkl(self, key):
        """
        load a pkl file (as a tuple)

        :param key:
        :return:
        """
        return self.logger.read_pkl(os.path.join(self.prefix, key))

    def load_np(self, key):
        """ load a np file

        :param key:
        :return:
        """
        return self.logger.read_np(os.path.join(self.prefix, key))

    @staticmethod
    def plt2data(fig):
        """

        @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
        @param fig a matplotlib figure
        @return a numpy 3D array of RGBA values
        """
        # draw the renderer
        fig.canvas.draw_idle()  # need this if 'transparent=True' to reset colors
        fig.canvas.draw()
        # Get the RGBA buffer from the figure
        w, h = fig.canvas.get_width_height()
        buf = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8)
        buf.shape = (h, w, 3)
        # todo: use alpha RGB instead
        # buf.shape = (h, w, 4)
        # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
        # buf = np.roll(buf, 4, axis=2)
        return buf

    def log_json(self):
        raise NotImplementedError

    def print(self, *args, sep=' ', end='\n', silent=False, flush=False):
        text = sep.join([str(a) for a in args]) + end
        try:
            self.print_buffer += text
        except:
            self.print_buffer = text
        if not silent:
            print(*args, sep=sep, end=end)
        if flush or len(self.print_buffer) > self.print_buffer_size:
            self.print_flush()

    def print_flush(self):
        try:
            text = self.print_buffer
        except:
            text = ""
        self.print_buffer = ""
        if text:
            self.log_text(text, silent=True)

    def log_text(self, text, filename="text.log", silent=False):
        # todo: consider adding step to this
        if not silent:
            print(text)
        self.logger.log_text(key=os.path.join(self.prefix or "", filename), text=text)


logger = ML_Logger()
