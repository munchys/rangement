# - * - encoding: UTF-8 -*-
from os import *
import mimetypes
import re
from gi.repository import Gtk
import glob
def rangement(dir):
	audiosdir = path.expanduser('~')+'/Musique/'
	videosdir = path.expanduser('~')+'/Vidéos/'
	imagesdir = path.expanduser('~')+'/Images/'
	documentsdir = path.expanduser('~')+'/Documents/'
	archivesdir =  path.expanduser('~')+'/Archives/'
	listregex = {"musiques":  re.compile('^audio/*'),
			"images": re.compile('^image/*'),
			'videos': re.compile('^video/*'),
	'documents' : re.compile('^application/(pdf|vnd*)'),
	'archives' : re.compile('^application/(zip|x-tar|rar)')
}
	chdir(dir)
	listnumfilemoved = {"musiques": 0,"archives": 0 ,
			"documents":0,"images":0,
			"videos": 0}
	for file in listdir('.'):
		filemimetype = str(mimetypes.guess_type(file)[0])
		print(filemimetype)
 		if listregex['documents'].match(filemimetype) :
			rename(file,documentsdir+file)
			listnumfilemoved['Documents'] += 1
 		elif listregex['images'].match(filemimetype) :
			rename(file,imagesdir+file)
			listnumfilemoved['images']+= 1
 		elif listregex['videos'].match(filemimetype) :
			rename(file,videosdir+file)
			listnumfilemoved["videos"] += 1
		elif listregex['archives'].match(filemimetype) :
			renames(file,archivesdir+file)
			listnumfilemoved["archives"] += 1
		elif listregex['musiques'].match(filemimetype):
			rename(file,audiosdir+file)
			listnumfilemoved["musiques"] += 1
 
	return listnumfilemoved

class MyWindow(Gtk.Window):
	dir = ''
	def __init__(self):
        	Gtk.Window.__init__(self, title="rangement")
		
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
		#combo box
		dir_combo = Gtk.ComboBoxText()
		dir_combo.connect("changed",self.on_dir_combo_changed)
		for file in glob.glob(path.expanduser("~")+'/*'):
			dir_combo.append_text(file)
#		dir_combo.set_entry_text_column(0)
		vbox.pack_start(dir_combo,False,False,True)
		self.label = Gtk.Label()
		vbox.pack_start(self.label,True,True,0)	
		#button
        	self.button = Gtk.Button(label="Lancer le rangement")
        	self.button.connect("clicked", self.on_button_clicked)
       		vbox.pack_start(self.button,False,False,True)
		self.add(vbox)

	def on_button_clicked(self, widget):
 		numfilemoved = rangement(self.dir)
		text= ''
		for files,num in numfilemoved.items():
			print(files+":"+str(num))
			text += files+':'+str(num)+"\n"
		self.label.set_text(text)

	def on_dir_combo_changed(self,widget):
		text = widget.get_active_text()
		if text != None:
			self.dir = text
if __name__ == "__main__":

    win = MyWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
