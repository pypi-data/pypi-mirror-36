"""
A customized logger for pyppl
"""
import logging, re, sys
from .utils import Box
from .exception import LoggerThemeError
from .templates import TemplatePyPPL
from multiprocessing import Value

# the entire format
LOGFMT = "[%(asctime)s]%(message)s"
# colors
COLORS = Box({
	'none'      : '',
	'end'       : '\033[0m',
	'bold'      : '\033[1m',
	'underline' : '\033[4m',

	# regular colors
	'black'     : '\033[30m',   'red'       : '\033[31m',	'green'     : '\033[32m',	'yellow'    : '\033[33m',
	'blue'      : '\033[34m',   'magenta'   : '\033[35m',   'cyan'      : '\033[36m',   'white'     : '\033[37m',
	# bgcolors
	'bgblack'   : '\033[40m',   'bgred'     : '\033[41m',   'bggreen'   : '\033[42m',   'bgyellow'  : '\033[43m',
	'bgblue'    : '\033[44m',   'bgmagenta' : '\033[45m',   'bgcyan'    : '\033[46m',   'bgwhite'   : '\033[47m',
})
# the themes
# keys:
# - no colon: match directory
# - in: from the the list
# - starts: startswith the string
# - re: The regular expression to match
# - has: with the string in flag
THEMES = {
	'greenOnBlack': {
		'DONE'    : COLORS.bold + COLORS.green,
		'DEBUG'   : COLORS.bold + COLORS.black,
		'PROCESS' : [COLORS.bold + COLORS.cyan, COLORS.bold + COLORS.cyan],
		'DEPENDS' : COLORS.magenta,
		'in:SUBMIT,JOBDONE,INFO,P.PROPS,OUTPUT,EXPORT,INPUT,P.ARGS,BRINGS': COLORS.green,
		'has:ERR' : COLORS.red,
		'in:WARNING,RETRY' : COLORS.bold + COLORS.yellow,
		'in:CACHED,RUNNING,SKIPPED,RESUMED': COLORS.yellow,
		''        : COLORS.white
	},
	'blueOnBlack':  {
		'DONE'    : COLORS.bold + COLORS.blue,
		'DEBUG'   : COLORS.bold + COLORS.black,
		'PROCESS' : [COLORS.bold + COLORS.cyan, COLORS.bold  + COLORS.cyan],
		'DEPENDS' : COLORS.green,
		'in:SUBMIT,JOBDONE,INFO,P.PROPS,OUTPUT,EXPORT,INPUT,P.ARGS,BRINGS': COLORS.blue,
		'has:ERR' : COLORS.red,
		'in:WARNING,RETRY' : COLORS.bold + COLORS.yellow,
		'in:CACHED,RUNNING,SKIPPED,RESUMED': COLORS.yellow,
		''        : COLORS.white
	},
	'magentaOnBlack':  {
		'DONE'    : COLORS.bold + COLORS.magenta,
		'DEBUG'   : COLORS.bold + COLORS.black,
		'PROCESS' : [COLORS.bold + COLORS.green, COLORS.bold + COLORS.green],
		'DEPENDS' : COLORS.blue,
		'in:SUBMIT,JOBDONE,INFO,P.PROPS,OUTPUT,EXPORT,INPUT,P.ARGS,BRINGS': COLORS.magenta,
		'has:ERR' : COLORS.red,
		'in:WARNING,RETRY' : COLORS.bold + COLORS.yellow,
		'in:CACHED,RUNNING,SKIPPED,RESUMED': COLORS.yellow,
		''        : COLORS.white
	},
	'greenOnWhite': {
		'DONE'    : COLORS.bold + COLORS.green,
		'DEBUG'   : COLORS.bold + COLORS.black,
		'PROCESS' : [COLORS.bold + COLORS.blue, COLORS.bold + COLORS.blue],
		'DEPENDS' : COLORS.magenta,
		'in:SUBMIT,JOBDONE,INFO,P.PROPS,OUTPUT,EXPORT,INPUT,P.ARGS,BRINGS': COLORS.green,
		'has:ERR' : COLORS.red,
		'in:WARNING,RETRY' : COLORS.bold + COLORS.yellow,
		'in:CACHED,RUNNING,SKIPPED,RESUMED': COLORS.yellow,
		''        : COLORS.black
	},
	'blueOnWhite':  {
		'DONE'    : COLORS.bold + COLORS.blue,
		'DEBUG'   : COLORS.bold + COLORS.black,
		'PROCESS' : [COLORS.bold + COLORS.green, COLORS.bold + COLORS.green],
		'DEPENDS' : COLORS.magenta,
		'in:SUBMIT,JOBDONE,INFO,P.PROPS,OUTPUT,EXPORT,INPUT,P.ARGS,BRINGS': COLORS.blue,
		'has:ERR' : COLORS.red,
		'in:WARNING,RETRY' : COLORS.bold + COLORS.yellow,
		'in:CACHED,RUNNING,SKIPPED,RESUMED': COLORS.yellow,
		''        : COLORS.black
	},
	'magentaOnWhite':  {
		'DONE'    : COLORS.bold + COLORS.magenta,
		'DEBUG'   : COLORS.bold + COLORS.black,
		'PROCESS' : [COLORS.bold + COLORS.blue, COLORS.bold + COLORS.blue],
		'DEPENDS' : COLORS.green,
		'in:SUBMIT,JOBDONE,INFO,P.PROPS,OUTPUT,EXPORT,INPUT,P.ARGS,BRINGS': COLORS.magenta,
		'has:ERR' : COLORS.red,
		'in:WARNING,RETRY' : COLORS.bold + COLORS.yellow,
		'in:CACHED,RUNNING,SKIPPED,RESUMED': COLORS.yellow,
		''        : COLORS.black
	}
}

LEVELS = {
	'all':     ['INPUT', 'OUTPUT', 'BRINGS', 'SUBMIT', 'P.ARGS', 'P.PROPS', 'JOBDONE', 'DEBUG'],
	'basic':   [],
	'normal':  ['INPUT', 'OUTPUT', 'BRINGS', 'SUBMIT', 'P.ARGS', 'P.PROPS'],
	'nodebug': ['INPUT', 'OUTPUT', 'BRINGS', 'SUBMIT', 'P.ARGS', 'P.PROPS', 'JOBDONE']
}

LEVELS_ALWAYS = ['PROCESS', 'SKIPPED', 'RESUMED', 'DEPENDS', 'STDOUT', 'STDERR', 'WARNING', 'ERROR', 'INFO', 'DONE', 'RUNNING', 'CACHED', 'EXPORT', 'PYPPL', 'TIPS', 'CONFIG', 'CMDOUT', 'CMDERR', 'RETRY']

def _getLevel (record):
	"""
	Get the flags of a record
	@params:
		`record`:  The logging record
	"""
	level = record.levelname
	msg   = record.msg.lstrip()
	m     = re.match(r'\[\s*([\w>._]+)\s*\](.*)', record.msg)
	if m:
		level = m.group(1).upper()
		msg   = m.group(2).lstrip()
	return (level, msg)

def _getColorFromTheme (level, theme):
	"""
	Get colors from a them
	@params:
		`level`: Our own log record level
		`theme`: The theme
	@returns:
		The colors
	"""
	ret = theme[''] if isinstance(theme[''], list) else [theme['']] * 2
	level = level.upper()
	
	for key, val in theme.items():
		if not isinstance(val, list):
			val = [val] * 2
		if key == level or \
		   key.startswith('in:') and level in key[3:].split(',') or \
		   key.startswith('starts:') and level.startswith(key[7:]) or \
		   key.startswith('has:') and key[4:] in level or \
		   key.startswith('re:') and re.search(key[3:], level):
			ret = val
			break
	return tuple(ret)
	
def _formatTheme(theme):
	"""
	Make them in the standard form with bgcolor and fgcolor in raw terminal color strings
	If the theme is read from file, try to translate "COLORS.xxx" to terminal color strings
	@params:
		`theme`: The theme
	@returns:
		The formatted colors
	"""
	if theme is True:
		theme = THEMES['greenOnBlack']
	if not theme:
		return False
	if not isinstance(theme, dict):
		raise LoggerThemeError(theme, 'No such theme')
	
	ret = {'': [COLORS.white, COLORS.white]}
	for key, val in theme.items():
		if not isinstance(val, list):
			val = [val]
		if len(val) == 1:
			val = val * 2

		for i, v in enumerate(val):
			t = TemplatePyPPL(v, colors = COLORS)
			val[i] = t.render()

		ret[key] = val
	return ret
	
class PyPPLLogFilter (logging.Filter):
	"""
	logging filter by levels (flags)
	"""
	
	def __init__(self, name='', lvls='normal', lvldiff=None):
		"""
		Constructor
		@params:
			`name`: The name of the logger
			`lvls`: The levels of records to keep
			`lvldiff`: The adjustments to `lvls`
		"""
		logging.Filter.__init__(self, name)
		if not isinstance(lvls, list):
			if lvls in LEVELS:
				self.levels = LEVELS[lvls]
			elif lvls == 'ALL':
				self.levels = LEVELS['all']
			elif lvls:
				self.levels = [lvls]
			else:
				self.levels = lvls
		else:
			self.levels = lvls

		if self.levels is False: return

		if self.levels is not None:
			self.levels += LEVELS_ALWAYS
			self.levels = list(set(self.levels))
		else:
			self.levels = []
			
		lvldiff = lvldiff or []
		for ld in lvldiff:
			if ld.startswith('-'):
				ld = ld[1:].upper()
				if ld in self.levels: 
					del self.levels[self.levels.index(ld)]
			elif ld.startswith('+'):
				ld = ld[1:].upper()
				if ld not in self.levels:
					self.levels.append(ld)
			else:
				ld = ld.upper()
				if ld not in self.levels:
					self.levels.append(ld)
	
	def filter (self, record):
		"""
		Filter the record
		@params:
			`record`: The record to be filtered
		@return:
			`True` if the record to be kept else `False`
		"""
		level   = _getLevel(record)[0]
		return self.levels and ( level in self.levels or level.startswith('_') )

class PyPPLLogFormatter (logging.Formatter):
	"""
	logging formatter for pyppl
	"""
	def __init__(self, fmt=None, theme='greenOnBlack', secondary = False):
		"""
		Constructor
		@params:
			`fmt`      : The format
			`theme`    : The theme
			`secondary`: Whether this is a secondary formatter or not (another formatter applied before this).
		"""
		fmt = LOGFMT if fmt is None else fmt
		logging.Formatter.__init__(self, fmt, "%Y-%m-%d %H:%M:%S")
		self.theme     = theme
		# whether it's a secondary formatter (for fileHandler)
		self.secondary = secondary
		
	
	def format(self, record):
		"""
		Format the record
		@params:
			`record`: The log record
		@returns:
			The formatted record
		"""
		(level, msg) = _getLevel(record)
		theme = 'greenOnBlack' if self.theme is True else self.theme
		theme = THEMES[theme] if not isinstance(theme, dict) and theme in THEMES else theme
		theme = _formatTheme(theme)

		if not theme:
			colorLevelStart = COLORS.none
			colorLevelEnd   = COLORS.none
			colorMsgStart   = COLORS.none
			colorMsgEnd     = COLORS.none
		else:
			(colorLevelStart, colorMsgStart) = _getColorFromTheme(level, theme)
			colorLevelEnd   = COLORS.end
			colorMsgEnd     = COLORS.end
		
		if self.secondary:
			# keep _ for file handler
			level = level[1:] if level.startswith('_') else level
		level = level[:7]
		record.msg = "[%s%7s%s] %s%s%s" % (colorLevelStart, level, colorLevelEnd, colorMsgStart, msg, colorMsgEnd)

		return logging.Formatter.format(self, record)

class PyPPLStreamHandler(logging.StreamHandler):
	"""
	PyPPL stream log handler.
	To implement the progress bar for JOBONE and SUBMIT logs.
	"""

	def __init__(self, stream = None):
		"""
		Constructor
		@params:
			`stream`: The stream
		"""
		self.pbar_started = Value('i', 0)
		super(PyPPLStreamHandler, self).__init__(stream)

	def _emit(self, record, terminator = "\n"):
		"""
		Helper function implementing a python2,3-compatible emit.
		Allow to add "\n" or "\r" as terminator.
		"""
		if sys.version_info[0] > 2: # pragma: no cover
			self.terminator = terminator
			super(PyPPLStreamHandler, self).emit(record)
		else:
			try:
				msg = self.format(record)
				stream = self.stream
				fs = "%s" + terminator
				#if no unicode support...
				if not logging._unicode: # pragma: no cover
					stream.write(fs % msg)
				else:
					try:
						if (isinstance(msg, unicode) and
							getattr(stream, 'encoding', None)): # pragma: no cover
							ufs = u'%s' + terminator
							try:
								stream.write(ufs % msg)
							except UnicodeEncodeError:
								#Printing to terminals sometimes fails. For example,
								#with an encoding of 'cp1251', the above write will
								#work if written to a stream opened or wrapped by
								#the codecs module, but fail when writing to a
								#terminal even when the codepage is set to cp1251.
								#An extra encoding step seems to be needed.
								stream.write((ufs % msg).encode(stream.encoding))
						else:
							stream.write(fs % msg)
					except UnicodeError: # pragma: no cover
						stream.write(fs % msg.encode("UTF-8"))
				self.flush()
			except (KeyboardInterrupt, SystemExit): # pragma: no cover
				raise
			except Exception: # pragma: no cover
				self.handleError(record)

	def emit(self, record):
		"""
		Emit the record.
		"""
		level, _ = _getLevel(record)
		if level in ['SUBMIT', 'JOBDONE']:
			self.pbar_started.value = 1
			terminator = "\r"
		else:
			terminator = "\n"
			if self.pbar_started.value == 1:
				self.stream.write('\n')
				self.pbar_started.value = 0
		self._emit(record, terminator)


def getLogger (levels='normal', theme=True, logfile=None, lvldiff=None, pbar = 'expand', name='PyPPL'):
	"""
	Get the default logger
	@params:
		`levels`: The log levels(tags), default: basic
		`theme`:  The theme of the logs on terminal. Default: True (default theme will be used)
			- False to disable theme
		`logfile`:The log file. Default: None (don't white to log file)
		`lvldiff`:The diff levels for log
			- ["-depends", "jobdone", "+debug"]: show jobdone, hide depends and debug
		`name`:   The name of the logger, default: PyPPL
	@returns:
		The logger
	"""
	logger    = logging.getLogger (name)
	for handler in logger.handlers:
		handler.close()
	del logger.handlers[:]
	
	if logfile:
		fileCh = logging.FileHandler(logfile)
		fileCh.setFormatter(PyPPLLogFormatter(theme = None))
		logger.addHandler (fileCh)
		
	streamCh  = PyPPLStreamHandler() if pbar != 'expand' else logging.StreamHandler()
	formatter = PyPPLLogFormatter(theme = theme, secondary = True)
	filter    = PyPPLLogFilter(name = name, lvls = levels, lvldiff = lvldiff)
	streamCh.addFilter(filter)
	streamCh.setFormatter(formatter)
	logger.addHandler (streamCh)
	
	logger.setLevel(1)
	# Output all logs
	return logger
	
logger = getLogger()