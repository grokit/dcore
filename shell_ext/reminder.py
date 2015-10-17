
import argparse
import time
import base64

import dcore.system_description as private_data
import dcore.shell_ext.gmail as gmail

_meta_shell_command = 'reminder'

def getArgs():
	
	parser = argparse.ArgumentParser()
	
	parser.add_argument('subject', nargs='+')
	parser.add_argument('-t', '--to', default= private_data.primary_email)
	parser.add_argument('-b', '--body', default='')
	parser.add_argument('-a', '--attachment')
	parser.add_argument('-w', '--work_email', action='store_true', default=False, help='Send to work e-mail instead of default one.')
	
	args = parser.parse_args()
	return args

def attachToBody(toAttach, originBody):
	abytes = open(toAttach, 'rb').read()
	return originBody + "\n\n ** Attachment: %s ** \n\n%s" % (toAttach, base64.b64encode(abytes))
	
if __name__ == '__main__':
	
	args = getArgs()
	print(args)
	
	if args.attachment is not None:
		args.body = attachToBody(args.attachment, args.body)
	
	if args.work_email:
		args.to = private_data.email_work 

	gmail.do(args.to, " ".join(args.subject), args.body)
