import glob
import os
import subprocess
import threading
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty

albums = []
movies = []
current_layout = None
is_playing = False
is_paused = False

class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)

class movie(object):
	def __init__(self, name):
		self.name = name.title()
		temp_name = name.replace(" ", "_")
		self.filepath = '/media/pi/LEXAR/movies/%s' % (temp_name) 
		
		videos = glob.glob(self.filepath+"/*.mp4") # This needs to be better. Can't guarantee file is always .mp4
		if len(videos) > 0:
			self.video = videos[0]
		elif len(videos) == 0:
			self.video = None

		posters = glob.glob(self.filepath+"/*.jpg") + glob.glob(self.filepath+"/*.png")
		if len(posters) > 0:
			self.poster = posters[0]
		else:
			self.poster = 'not_found.gif'

def get_movies():
	'Search USB drive for movies and create movie objects for each movie found'
	global movies
	for root, dirs, files in os.walk("/media/pi/LEXAR/movies"):
		for dir in dirs:
			if dir[0] != ".":
				new_movie = movie(dir.replace("_", " "))
				if any(temp_movie.name == new_movie.name for temp_movie in movies):
					continue
				else:
					print '[INFO] Adding new movie'
					movies.append(new_movie)

def return_movie(mov_string):
	'Returns movie object if movie name is found in movie list, otherwise returns None'
	for movie in movies:
		if mov_string == movie.name:
			return movie
	return None

Builder.load_string('''
<Movie>:

<Controller>:
    BoxLayout:
        id: bl
        orientation: 'vertical'
        size: root.width, root.height
        padding: 10, 10
        row_default_height: '48dp'
        row_force_default: True
        spacing: 10, 10
        AnchorLayout:
            anchor_x: 'right'
            anchor_y: 'top'
            Button:
                on_release: root.manager.current_screen.xit()
                text: 'X'
                size_hint: None, None
                size: 50, 50
        TabbedPanel:
            id: tp_main
            do_default_tab: False

            TabbedPanelItem:
                id: movies_tab
                text: 'Movies'
                TabbedPanel:
                    id: mov_alph_tp
                    do_default_tab: False

                    TabbedPanelItem:
                        id: mov_all
                        text: 'All'
                        on_release: root.manager.current_screen.show_movies_all(mov_all_content)

                        ScrollView:
                            id: mov_all_sv
                            size: self.size

                            GridLayout:
                                id: mov_all_content
                                size_hint_y: None
                                size: root.width, root.height - 20
                                cols: 3
                                row_default_width: 175
                                row_default_height: 200
                                row_force_default: True
                    TabbedPanelItem:
                        id: mov_a_g
                        text: 'A - G'
                        on_release: root.manager.current_screen.show_movies_a_g(mov_a_g_content)

                        ScrollView:
                            size: self.size

                            GridLayout:
                                id: mov_a_g_content
                                size_hint_y: None
                                size: root.width, root.height - 20
                                cols: 3
                                row_default_width: 175
                                row_default_height: 200
                                row_force_default: True
                    TabbedPanelItem:
                        id: mov_h_n
                        text: 'H - N'
                        on_release: root.manager.current_screen.show_movies_h_n(mov_h_n_content)

                        ScrollView:
                            size: self.size

                            GridLayout:
                                id: mov_h_n_content
                                size_hint_y: None
                                size: root.width, root.height - 20
                                cols: 3
                                row_default_width: 175
                                row_default_height: 200
                                row_force_default: True
                    TabbedPanelItem:
                        id: mov_o_u
                        text: 'O - U'
                        on_release: root.manager.current_screen.show_movies_o_u(mov_o_u_content)

                        ScrollView:
                            size: self.size

                            GridLayout:
                                id: mov_o_u_content
                                size_hint_y: None
                                size: root.width, root.height - 20
                                cols: 3
                                row_default_width: 175
                                row_default_height: 200
                                row_force_default: True
                    TabbedPanelItem:
                        id: mov_v_z
                        text: 'V - Z'
                        on_release: root.manager.current_screen.show_movies_v_z(mov_v_z_content)

                        ScrollView:
                            size: self.size

                            GridLayout:
                                id: mov_v_z_content
                                size_hint_y: None
                                size: root.width, root.height - 20
                                cols: 3
                                row_default_width: 175
                                row_default_height: 200
                                row_force_default: True

            TabbedPanelItem:
                id: music_tab
                text: 'Music'
                on_release: root.manager.current_screen.show_music(music_content)
                ScrollView:
                    size: self.size

                    GridLayout:
                        id: music_content
                        size_hint_y: None
                        size: root.width, root.height - 20
                        cols: 3
                        row_default_height: '20dp'
                        row_force_default: True
''')

class Movie(Screen):
	global root
	current_movie = ""
	play_button = StringProperty()
	
	def __init__(self, **kwargs):
                super(Movie, self).__init__(**kwargs)
		self.play_button = "||"

	def change_button(self, text):
                self.play_button = text

	def select_movie(self, movie):
		'Finds movie to play based on selected choice, changes widget screen to movie, and plays movie if available'
		global is_playing
		global is_paused
		movie = return_movie(movie)
		if movie.video == None:
			content = GridLayout(cols=1)
    			content_cancel = Button(text='Close', size_hint_y=None, height=40)
    			content.add_widget(Label(text='Video file missing for this movie! Please try again later'))
    			content.add_widget(content_cancel)
			popup = Popup(title='Video Missing',
				content=content,
				size_hint=(None, None), size=(400, 400))
			content_cancel.bind(on_release=popup.dismiss)
			popup.open()
		else:
			root.current = 'movie'
			if self.current_movie != movie:
				if os.path.isfile('movie_fifo'):
					self.quit_movie(movie)
				self.play_button = "||"
				self.current_movie = movie
				root.current_screen.clear_widgets()
				subprocess.Popen(['/usr/bin/killall', 'omxplayer.bin'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
				subprocess.Popen(['/usr/bin/killall', 'load_movie.sh'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
				print '[INFO] Loading movie'
				subprocess.Popen(['./scripts/load_movie.sh', movie.video])
                		root.current_screen.add_widget(Builder.load_string('''
BoxLayout:
    id: 'mov_bl'
    orientation: 'vertical'
    AnchorLayout:
        anchor_x: 'left'
        anchor_y: 'top'
        Button:
            on_release: app.root.current = "controller"
            text: 'X'
            size_hint: None, None
            size: 50, 50
    Image:
        source: '%s'
        size_hint_y: None
        height: 350
        keep_ratio: True
        center_x: self.parent.center_x
        center_y: self.parent.center_y
    AnchorLayout:
        id: 'mov_al'
        anchor_x: 'center'
        anchor_y: 'bottom'
        BoxLayout:
            orientation: 'horizontal'
            Button:
                id: 'skip_back_button'
                on_release: app.root.current_screen.skip_back_movie('%s')
                text: '|<<'
                size: 50, 50
            Button:
                on_release: app.root.current_screen.rewind_movie('%s')
                id: 'rw_button'
                text: '<<'
                size: 50, 50
            Button:
                id: 'play_button'
                on_release: app.root.current_screen.play_movie('%s')
                text: app.root.current_screen.play_button
                size: 50, 50
            Button:
                id: 'ff_button'
                on_release: app.root.current_screen.fast_forward_movie('%s')
                text: '>>'
                size: 50, 50
            Button:
                id: 'skip_for_button'
                on_release: app.root.current_screen.skip_forward_movie('%s')
                text: '>>|'
                size: 50, 50
''' % (movie.poster, movie.name, movie.name, movie.name, movie.name, movie.name)))
				self.play(movie)
				is_playing = True
				is_paused = False

	def play(self, movie):
		'Call "play_movie.sh" script to play movie'
		movie = return_movie(movie)
		# Start the new movie
		print '[INFO] Playing movie'
		self.change_button("||")
		subprocess.Popen('./scripts/play_movie.sh')

	def pause_resume(self, movie):
		'Call "play_pause_movie.sh" script to play/pause movie'
		subprocess.Popen('./scripts/play_pause_movie.sh')
		
        def play_movie(self, movie):
		'Checks if movie is currently paused or playing, updates button text accoringly, and plays/pauses movie'
		global is_paused
		global is_playing
		if is_paused:
			is_paused = False
			is_playing = True
			self.change_button("||") #Changes it to '||'
			print '[INFO] Resuming movie'
		else:
			is_paused = True
			is_playing = False
			print '[INFO] Pausing movie'
			self.change_button(">") #Changes it to '>'

		self.pause_resume(movie)

	def skip_back_movie(self, movie):
		print '[INFO] Skipping back movie'
		subprocess.Popen('./scripts/skip_backwards_movie.sh')

	def rewind_movie(self, movie):
		global is_playing
		global is_paused
		print '[INFO] Rewinding movie'
		subprocess.Popen('./scripts/rewind_movie.sh')
		if self.is_playing:
			self.change_button(">")
			is_playing = False
			is_paused = True

	def fast_forward_movie(self, movie):
		global is_playing
                global is_paused
		print '[INFO] Fast forwarding movie'
		subprocess.Popen('./scripts/fast_forward_movie.sh')
		if is_paused == True:
                        self.change_button("||")
                        is_playing = True
                        is_paused = False

	def skip_forward_movie(self, movie):
		print '[INFO] Skipping forward movie'
		subprocess.Popen('./scripts/skip_forward_movie.sh')

	def quit_movie(self, movie):
		print '[INFO] Quitting movie'
		subprocess.Popen('./scripts/quit_movie.sh')

class Controller(Screen):
	global movies
	mov = Movie()
        def update(self, dt):
                self.check_new_movies()
                #self.check_new_music

	def xit(self):
        	subprocess.Popen(['/usr/bin/killall', 'omxplayer.bin'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        	subprocess.Popen(['/usr/bin/killall', 'load_movie.sh'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        	exit()

	def check_new_movies(self):
                old_size = len(movies)
                get_movies()
                if len(movies) != old_size:
                        if current_layout == "mov_all_content":
                                self.show_movies_all(current_layout)
                        elif current_layout == "mov_a_g_content":
                                self.show_movies_a_g(current_layout)
                        elif current_layout == "mov_h_n_content":
                                self.show_movies_h_n(current_layout)
                        elif current_layout == "mov_o_u_content":
                                self.show_movies_o_u(current_layout)
                        elif current_layout == "mov_v_z_content":
                                self.show_movies_v_z(current_layout)
                        else:
                                pass

        def check_new_music(self):
                pass
                #Eventually add this code in
                #old_size = len(albums)
                #update and grab new albums here
                #if len(albums) != old_size:
                #        if current_layout == "alb_all_content":
                #                self.show_movies_all(current_layout)
                #        elif current_layout == "alb_a_g_content":
                #                self.show_movies_a_g(current_layout)
                #        elif current_layout == "alb_h_n_content":
                #                self.show_movies_h_n(current_layout)
                #        elif current_layout == "alb_o_u_content":
                #                self.show_movies_o_u(current_layout)
                #        elif current_layout == "alb_v_z_content":
                #                self.show_albums_v_z(current_layout)
                #        else:
                #                pass

	def select_movie(self, movie):
		self.mov.select_movie(movie)

        def show_movies_all(self, layout):
                global current_layout
                current_layout = layout
                layout.clear_widgets()
                for movie in movies:
                        layout.add_widget(Builder.load_string('''
Button:
    on_release: app.root.current_screen.select_movie('%s')
    text: '%s'
    text_size: self.size
    halign: 'center'
    valign: 'bottom'
    Image:
        source: '%s'
        size_hint_y: None
        height: 190
        keep_ratio: True
        center_x: self.parent.center_x
        center_y: self.parent.center_y + 10

''' % (movie.name, movie.name, movie.poster)))

        def show_movies_a_g(self, layout):
                global current_layout
                current_layout = layout
                layout.clear_widgets()
                for movie in movies:
                        letter = ord(movie.name[0].lower())
                        if (letter >= ord('a')) and (letter <= ord('g')): 
                                layout.add_widget(Builder.load_string('''
Button:
    on_release: app.root.current_screen.select_movie('%s')
    text: '%s'
    text_size: self.size
    halign: 'center'
    valign: 'bottom'
    Image:
        source: '%s'
        size_hint_y: None
        height: 190
        keep_ratio: True
        center_x: self.parent.center_x
        center_y: self.parent.center_y

''' % (movie.name, movie.name, movie.poster)))

        def show_movies_h_n(self, layout):
                global current_layout
                current_layout = layout
                layout.clear_widgets()
                for movie in movies:
                        letter = ord(movie.name[0].lower())
                        if (letter >= ord('h')) and (letter <= ord('n')):
                                layout.add_widget(Builder.load_string('''
Button:
    on_release: app.root.current_screen.select_movie('%s')
    text: '%s'
    text_size: self.size
    halign: 'center'
    valign: 'bottom'
    Image:
        source: '%s'
        size_hint_y: None
        height: 190
        keep_ratio: True
        center_x: self.parent.center_x
        center_y: self.parent.center_y

''' % (movie.name, movie.name, movie.poster)))

        def show_movies_o_u(self, layout):
                global current_layout
                current_layout = layout
                layout.clear_widgets()
                for movie in movies:
                        letter = ord(movie.name[0].lower())
                        if (letter >= ord('o')) and (letter <= ord('u')):
                                layout.add_widget(Builder.load_string('''
Button:
    on_release: app.root.current_screen.select_movie('%s')
    text: '%s'
    text_size: self.size
    halign: 'center'
    valign: 'bottom'
    Image:
        source: '%s'
        size_hint_y: None
        height: 190
        keep_ratio: True
        center_x: self.parent.center_x
        center_y: self.parent.center_y

''' % (movie.name, movie.name, movie.poster)))

        def show_movies_v_z(self, layout):
                global current_layout
                current_layout = layout
		layout.clear_widgets()
                for movie in movies:
                        letter = ord(movie.name[0].lower())
                        if (letter >= ord('v')) and (letter <= ord('z')):
                                layout.add_widget(Builder.load_string('''
Button:
    on_release: app.root.current_screen.select_movie('%s')
    text: '%s'
    text_size: self.size
    halign: 'center'
    valign: 'bottom'
    Image:
        source: '%s'
        size_hint_y: None
        height: 190
        keep_ratio: True
        center_x: self.parent.center_x
        center_y: self.parent.center_y

''' % (movie.name, movie.name, movie.poster)))

        def show_music(self, layout):
                pass

root = ScreenManager()

class ControllerApp(App):
	def build(self):
		global movies
		global root
		#movies = sorted(set(movies), key=lambda x: x.name)
		movies.sort(key=lambda x: x.name)
		root.add_widget(Controller(name='controller'))
		root.add_widget(Movie(name='movie'))
		root.current_screen.show_movies_all(root.current_screen.ids.mov_all_content)
		Clock.schedule_interval(root.current_screen.update, 30.0)
		return root

if __name__ == '__main__':
	get_movies()
	ControllerApp().run()
