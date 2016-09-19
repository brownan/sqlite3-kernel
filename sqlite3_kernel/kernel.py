from ipykernel.kernelbase import Kernel
from pexpect import replwrap, EOF

from subprocess import check_output

import re
import signal

__version__ = '0.2'

version_pat = re.compile(r'SQLite version (\d+(\.\d+)+)')

class Sqlite3REPL(replwrap.REPLWrapper):
    def __init__(self):
        super().__init__(
            "sqlite3",
            "sqlite> ",
            ".prompt {} {}",
        )
    def run_command(self, command, timeout=-1):
        """Same as parent class but on continuations, send a semicolon to
        terminate the command"""
        cmdlines = command.splitlines()
        if command.endswith('\n'):
            cmdlines.append('')
        if not cmdlines:
            raise ValueError("No command was given")

        res = []
        self.child.sendline(cmdlines[0])
        for line in cmdlines[1:]:
            self._expect_prompt(timeout=timeout)
            res.append(self.child.before)
            self.child.sendline(line)

        # Command was fully submitted, now wait for the next prompt
        if self._expect_prompt(timeout=timeout) == 1:
            # We got the continuation prompt - command was incomplete
            self.child.sendline(";")
            if self._expect_prompt(timeout=timeout) == 1:
                raise ValueError("Continuation prompt found - input was incomplete:\n"
                                 + command)
        return u''.join(res + [self.child.before])

class Sqlite3Kernel(Kernel):
    implementation = 'sqlite3_kernel'
    implementation_version = __version__

    @property
    def language_version(self):
        m = version_pat.search(self.banner)
        return m.group(1)

    _banner = None

    @property
    def banner(self):
        if self._banner is None:
            self._banner = check_output(['sqlite3', '--version']).decode('utf-8')
        return self._banner

    language_info = {'name': 'sqlite3',
                     'codemirror_mode': 'shell',
                     'mimetype': 'text/x-sh',
                     'file_extension': '.sql'}

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._start_sqlite()

    def _start_sqlite(self):
        # Signal handlers are inherited by forked processes, and we can't easily
        # reset it from the subprocess. Since kernelapp ignores SIGINT except in
        # message handlers, we need to temporarily reset the SIGINT handler here
        # so that sqlite is interruptable
        sig = signal.signal(signal.SIGINT, signal.SIG_DFL)
        try:
            self.sqlitewrapper = Sqlite3REPL()
        finally:
            signal.signal(signal.SIGINT, sig)

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        if not code.strip():
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

        interrupted = False
        try:
            output = self.sqlitewrapper.run_command(code.rstrip())
        except KeyboardInterrupt:
            self.sqlitewrapper.child.sendintr()
            interrupted = True
            self.sqlitewrapper._expect_prompt()
            output = self.sqlitewrapper.child.before
        except EOF:
            output = self.sqlitewrapper.child.before + 'Restarting SQLite3'
            self._start_sqlite()

        if not silent:
            # Send standard output
            stream_content = {'name': 'stdout', 'text': output}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        if interrupted:
            return {'status': 'abort', 'execution_count': self.execution_count}

        return {'status': 'ok', 'execution_count': self.execution_count,
                'payload': [], 'user_expressions': {}}

