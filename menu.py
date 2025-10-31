import os
import subprocess
import shutil
from datetime import datetime
from functools import partial

# --- ADD THIS IMPORT ---
from kivy.config import Config
# --- ADD THIS CONFIGURATION BLOCK ---
# Tell Kivy not to use a virtual keyboard, eliminating the info message
Config.set('kivy', 'keyboard_mode', 'system')
# 'system' means use the native OS input methods (i.e., your physical keyboard)
# --- END CONFIGURATION BLOCK ---

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import BooleanProperty

# --- CONFIG ---
PROJECTS_BASE = "rivy/projects"
DEFAULT_FOLDERS = ["assets", "scripts", "shaders","GUI state","world state","config"]
# Set the directory where your editor executables are located
EDITOR_BASE_PATH = "/home/sudais/Rivy-engine/editor/target/release/" 
# Set the *default* executable file name
DEFAULT_EDITOR_NAME = "editor"  
os.makedirs(PROJECTS_BASE, exist_ok=True)
# --- END MODIFIED ---

# --- AESTHETICS (Dark Theme) ---
COLOR_BG = (0.1, 0.1, 0.1, 1)        # Dark grey
COLOR_BG_LIGHT = (0.15, 0.15, 0.15, 1) # Lighter grey
COLOR_TEXT = (0.9, 0.9, 0.9, 1)
COLOR_PRIMARY = (0.0, 0.5, 0.8, 1)   # Blue
COLOR_SELECTED = (0.0, 0.35, 0.6, 1)  # Darker blue
COLOR_DANGER = (0.8, 0.2, 0.2, 1)    # Red

# Set app-wide background color
Window.clearcolor = COLOR_BG


class ProjectEntry(ButtonBehavior, BoxLayout):
    """
    A custom widget for the project list.
    It's a clickable BoxLayout that shows project info
    and changes color when selected.
    """
    selected = BooleanProperty(False)

    def __init__(self, project_name, modified_time, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=5, **kwargs)
        self.project_name = project_name
        
        self.add_widget(Label(
            text=project_name,
            font_size=18,
            halign='left',
            valign='top',
            color=COLOR_TEXT
        ))
        self.add_widget(Label(
            text=f"Last Modified: {modified_time}",
            font_size=12,
            halign='left',
            valign='top',
            color=(0.7, 0.7, 0.7, 1) # Light grey for subtext
        ))
        
        # Make labels respect the layout's size
        self.bind(size=self._update_label_text_size)

        # Draw the background
        with self.canvas.before:
            self.bg_color = Color(*COLOR_BG_LIGHT)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_label_text_size(self, instance, value):
        for child in self.children:
            child.text_size = (instance.width - 20, None) # 20 for padding

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_selected(self, instance, value):
        """ Update background color on selection change """
        if value:
            self.bg_color.rgba = COLOR_SELECTED
        else:
            self.bg_color.rgba = COLOR_BG_LIGHT

    def on_press(self):
        self.bg_color.rgba = COLOR_SELECTED

    def on_release(self):
        # The 'selected' property will be set by the parent,
        # which will then trigger on_selected to set the final color.
        pass


class ProjectManager(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)
        
        self.selected_project_name = None

        # --- Title ---
        self.add_widget(Label(
            text="[b]Rivy Engine Project Manager[/b]",
            markup=True,
            font_size=24,
            size_hint_y=None,
            height=40,
            color=COLOR_TEXT
        ))

        # --- Editor Path Bar (Top) ---
        editor_bar = BoxLayout(size_hint_y=None, height=40, spacing=10)
        editor_bar.add_widget(Label(
            text="Editor Name:",
            size_hint_x=None,
            width=100,
            color=COLOR_TEXT
        ))
        self.editor_input = TextInput(
            text=DEFAULT_EDITOR_NAME,  # Set default *name*
            multiline=False,
            size_hint_y=None,
            height=40,
            background_color=COLOR_BG_LIGHT,
            foreground_color=COLOR_TEXT
        )
        editor_bar.add_widget(self.editor_input)
        self.add_widget(editor_bar)

        # --- Main Content Area (Projects List + Actions Panel) ---
        main_layout = BoxLayout(orientation='horizontal', spacing=10)

        # --- Left Panel: Project List ---
        project_list_container = BoxLayout(orientation='vertical', size_hint_x=0.7)
        project_list_container.add_widget(Label(
            text="Projects",
            font_size=20,
            size_hint_y=None,
            height=30,
            color=COLOR_TEXT
        ))
        
        self.project_list_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.project_list_layout.bind(minimum_height=self.project_list_layout.setter("height"))

        scroll = ScrollView(bar_width=10, bar_color=COLOR_PRIMARY)
        scroll.add_widget(self.project_list_layout)
        project_list_container.add_widget(scroll)
        
        main_layout.add_widget(project_list_container)

        # --- Right Panel: Actions ---
        actions_panel = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_x=0.3
        )
        
        actions_panel.add_widget(Label(
            text="Create New Project",
            font_size=18,
            size_hint_y=None,
            height=30,
            color=COLOR_TEXT
        ))
        
        self.new_project_input = TextInput(
            hint_text="New project name...",
            multiline=False,
            size_hint_y=None,
            height=40,
            background_color=COLOR_BG_LIGHT,
            foreground_color=COLOR_TEXT
        )
        actions_panel.add_widget(self.new_project_input)
        
        self.make_btn = Button(
            text="Create Project",
            size_hint_y=None,
            height=50,
            background_normal='',
            background_color=COLOR_PRIMARY
        )
        self.make_btn.bind(on_release=self.make_project)
        actions_panel.add_widget(self.make_btn)
        
        # Spacer
        actions_panel.add_widget(Label(text='', size_hint_y=0.2)) 
        
        actions_panel.add_widget(Label(
            text="Selected Project",
            font_size=18,
            size_hint_y=None,
            height=30,
            color=COLOR_TEXT
        ))

        self.open_btn = Button(
            text="Open Selected",
            size_hint_y=None,
            height=50,
            background_normal='',
            background_color=COLOR_PRIMARY
        )
        self.open_btn.bind(on_release=self.open_project)
        actions_panel.add_widget(self.open_btn)

        self.delete_btn = Button(
            text="Delete Selected",
            size_hint_y=None,
            height=50,
            background_normal='',
            background_color=COLOR_DANGER # Red for delete
        )
        self.delete_btn.bind(on_release=self.delete_project)
        actions_panel.add_widget(self.delete_btn)
        
        # Spacer
        actions_panel.add_widget(Label(text='', size_hint_y=0.8)) 

        main_layout.add_widget(actions_panel)
        self.add_widget(main_layout)

        self.refresh_projects()

    def refresh_projects(self):
        self.project_list_layout.clear_widgets()
        if not os.path.exists(PROJECTS_BASE):
            return
            
        projects = []
        for name in sorted(os.listdir(PROJECTS_BASE)):
            path = os.path.join(PROJECTS_BASE, name)
            if os.path.isdir(path):
                try:
                    mtime = os.path.getmtime(path)
                    projects.append((name, mtime))
                except OSError:
                    continue # Skip if permissions error, etc.

        # Sort by modification time, newest first
        projects.sort(key=lambda p: p[1], reverse=True)

        for name, mtime in projects:
            path = os.path.join(PROJECTS_BASE, name)
            modified_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            entry = ProjectEntry(
                project_name=name,
                modified_time=modified_str,
                size_hint_y=None,
                height=70
            )
            # Use partial to pass the name to the select function
            entry.bind(on_release=partial(self.select_project, name))
            self.project_list_layout.add_widget(entry)
            
        self.select_project(None) # Deselect all

    def select_project(self, project_name, *args):
        self.selected_project_name = project_name
        
        # Update visuals for all project entries
        for entry in self.project_list_layout.children:
            if isinstance(entry, ProjectEntry):
                entry.selected = (entry.project_name == project_name)

    def make_project(self, _):
        name = self.new_project_input.text.strip()
        if not name:
            self.show_popup("Error", "Please enter a project name.")
            return

        project_path = os.path.join(PROJECTS_BASE, name)
        if os.path.exists(project_path):
            self.show_popup("Error", f"Project '{name}' already exists.")
            return

        os.makedirs(project_path)
        for folder in DEFAULT_FOLDERS:
            os.makedirs(os.path.join(project_path, folder), exist_ok=True)

        self.show_popup("Success", f"Project '{name}' created.")
        self.new_project_input.text = ""
        self.refresh_projects()
        
        # Select and open the newly created project
        self.select_project(name)
        self._launch_editor()

    def open_project(self, _):
        if not self.selected_project_name:
            self.show_popup("Error", "Please select a project to open.")
            return
        
        self._launch_editor()

    def _launch_editor(self):
        """ Internal helper to launch the editor with the selected project """
        if not self.selected_project_name:
            self.show_popup("Error", "No project selected to launch.")
            return

        project_path = os.path.join(PROJECTS_BASE, self.selected_project_name)

        # Get just the file name from the input
        editor_filename = self.editor_input.text.strip()
        if not editor_filename:
            self.show_popup("Error", "Editor executable name is empty.")
            return
            
        # Combine with the base path
        editor_path = os.path.join(EDITOR_BASE_PATH, editor_filename)


        if not os.path.exists(editor_path):
            # Show the full path in the error message for easy debugging
            self.show_popup("Warning", f"Editor executable not found at:\n{editor_path}")
            return
            
        if not os.path.exists(project_path):
             self.show_popup("Error", f"Project path does not exist:\n{project_path}")
             self.refresh_projects() # Project may have been deleted externally
             return

        try:
            subprocess.Popen([editor_path, project_path])
        except Exception as e:
            self.show_popup("Error", f"Failed to launch editor:\n{e}")

    def delete_project(self, _):
        name = self.selected_project_name
        if not name:
            self.show_popup("Error", "Please select a project to delete.")
            return

        project_path = os.path.join(PROJECTS_BASE, name)
        if not os.path.exists(project_path):
            self.show_popup("Error", f"Project '{name}' not found.")
            self.refresh_projects() # Sync list
            return
        
        try:
            shutil.rmtree(project_path)
            self.show_popup("Deleted", f"Project '{name}' deleted.")
            self.selected_project_name = None
            self.refresh_projects()
        except Exception as e:
            self.show_popup("Error", f"Could not delete project:\n{e}")

    def show_popup(self, title, message):
        # Styled popup
        content = Label(
            text=message,
            halign='center',
            valign='middle',
            color=COLOR_TEXT
        )
        content.bind(size=lambda *x: content.setter('text_size')(content, (380, None)))

        popup = Popup(
            title=title,
            title_color=COLOR_TEXT,
            content=content,
            size_hint=(None, None),
            size=(400, 200),
            separator_color=COLOR_PRIMARY
        )
        
        # Popup background
        with popup.canvas.before:
            Color(*COLOR_BG_LIGHT)
            Rectangle(pos=popup.pos, size=popup.size)
            
        popup.open()


class RivyMenuApp(App):
    def build(self):
        return ProjectManager()


if __name__ == "__main__":
    RivyMenuApp().run()
