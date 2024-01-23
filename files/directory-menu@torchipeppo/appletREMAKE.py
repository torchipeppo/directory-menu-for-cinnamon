"""/**
 * Cinnamon applet that attempts to replicate the functionality of the "Directory Menu" plugin from Xfce.
 * Written fron scratch, not strictly translating the code of said plugin, as the author's first experiment in Cinnamon development.
 * 
 * Took major cues from: Xfce's Directory Menu, Cinnamon's Favorites applet, and Nemo.
 * And of course the documentation for GLib/Gtk/Gdk/Gio.
 * 
 * "Cassettone" is the codename of this applet. (Italian for "large drawer".)
 * I didn't want to call it directly "Directory Menu" in the code,
 * since a "Menu" is an already existing concept here, i.e. a dropwown menu object.
 */"""

#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("GLib", "2.0")
gi.require_version('XApp', '1.0')

import os
import configparser
from gi.repository import Gio, Gtk, Gdk, GLib, XApp

UUID = 'directory-menu@torchipeppo'
APP_NAME = "Directory Menu"
APPLET_DIR = os.path.join(os.path.dirname(__file__))

# const Applet = imports.ui.applet
# const Util = imports.misc.util
# const GLib = imports.gi.GLib
# const Gtk = imports.gi.Gtk
# const Gdk = imports.gi.Gdk
# const Gio = imports.gi.Gio
# const Settings = imports.ui.settings





def populate_menu_with_directory(menu, directory_uri):
    directory = Gio.File.new_for_uri(directory_uri)
    # // First, the two directory actions: Open Folder and Open In Terminal

    open_item = Gtk.ImageMenuItem.new_with_label("Open Folder")
    open_image = Gtk.Image.new_from_icon_name("folder", Gtk.IconSize.MENU)
    open_item.set_image(open_image)
    open_item.connect("activate", lambda: launch(directory.get_uri(), Gtk.get_current_event_time()))
    menu.append(open_item)

    term_item = Gtk.ImageMenuItem.new_with_label("Open in Terminal")
    term_image = Gtk.Image.new_from_icon_name("terminal", Gtk.IconSize.MENU)
    term_item.set_image(term_image)
    term_item.connect("activate", lambda: open_terminal_at_path(directory.get_path()))
    menu.append(term_item)

    menu.append(Gtk.SeparatorMenuItem.new())

    # print(directory_uri)

    # iter = directory.enumerate_children('standard::*', Gio.FileQueryInfoFlags.NONE, None)

    # dirs = []
    # nondirs = []

    # info = iter.next_file(None)
    # while info != None:
    #     if (not info.get_is_hidden()):     # // <-- skip hidden files
    #         info.display_name = info.get_display_name()
    #         info.content_type = info.get_content_type()
    #         info.file = directory.get_child_for_display_name(info.display_name)
    #         info.is_directory = (info.get_content_type() == "inode/directory")

    #         if (info.is_directory):
    #             dirs.push(info)
    #         else:
    #             nondirs.push(info)

    #     info = iter.next_file(None)

    # dirs.sort(lambda a,b: strcmp_insensitive(a.display_name, b.display_name))
    # nondirs.sort(lambda a,b: strcmp_insensitive(a.display_name, b.display_name))

    # dirs.forEach(lambda info: add_to_menu_from_gioinfo(menu, info))
    # nondirs.forEach(lambda info: add_to_menu_from_gioinfo(menu, info))

# def add_to_menu_from_gioinfo(menu, info):
#     display_text = info.display_name

#     icon = Gio.content_type_get_icon(info.content_type)
#     image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.MENU)

#     uri = info.file.get_uri()

#     item = Gtk.ImageMenuItem.new_with_label(display_text)
#     item.set_image(image)

#     if info.is_directory:
#         subMenu = create_subdirectory_submenu(uri)
#         item.set_submenu(subMenu)
#     else:
#         item.connect("activate", lambda: launch(uri, Gtk.get_current_event_time()))

#     menu.append(item)

# def create_subdirectory_submenu(uri):
#     subMenu = Gtk.Menu.new()

#     def f():
#         populate_menu_with_directory(subMenu, uri)
#         subMenu.show_all()

#     subMenu.connect("show", f)

#     subMenu.connect("hide", lambda: destroy_all_children_later(subMenu))

#     return subMenu

# // essentially an independent JS translation of xapp_favorites_launch from the Favorites Xapp.
def launch(uri, timestamp):
    # let display = Gdk.Display.get_default()
    # let launch_context = display.get_app_launch_context()
    # launch_context.set_timestamp(timestamp)
    # Gio.AppInfo.launch_default_for_uri_async(uri, launch_context, null, this.launch_callback)
    print(f"Launch {uri}")

# // emulates how nemo handles opening in terminal (using the same flags as Util.spawn)
def open_terminal_at_path(path):
    # let gnome_terminal_preferences = Gio.Settings.new("org.cinnamon.desktop.default-applications.terminal")
    # let default_terminal = gnome_terminal_preferences.get_string("exec")
    # let argv = [default_terminal]
    # let spawn_flags = GLib.SpawnFlags.SEARCH_PATH
    #             | GLib.SpawnFlags.STDOUT_TO_DEV_NULL
    #             | GLib.SpawnFlags.STDERR_TO_DEV_NULL
    # GLib.spawn_async(path, argv, null, spawn_flags, null)
    print(f"Terminal at {path}")

# def launch_callback(source_object, result):
#     if not Gio.AppInfo.launch_default_for_uri_finish(result):
#         print("An error has occurred while launching an item of the Directory Menu.")

def destroy_all_children_later(menu):

    def g1(subItem):
        def g2():
            subItem.destroy()
            print("destroyed")
            return False
        # // destroy at some future instant, but not right now so we have time for the activate event
        GLib.idle_add(priority=GLib.PRIORITY_HIGH_IDLE, function=g2)

    menu.foreach(g1)

def strcmp_insensitive(a, b):
    a = a.lower()
    b = b.lower()
    if a < b: return -1
    if a > b: return 1
    return 0









def populate_menu_with_directory_2(menu, directory_uri):
    print(directory_uri)
    directory = Gio.File.new_for_uri(directory_uri)
    # // First, the two directory actions: Open Folder and Open In Terminal

    open_item = Gtk.MenuItem.new_with_label("Open Folder")
    open_item.connect("activate", lambda _: launch(directory.get_uri(), Gtk.get_current_event_time()))
    menu.append(open_item)

    term_item = Gtk.MenuItem.new_with_label("Open in Terminal")
    term_item.connect("activate", lambda _: open_terminal_at_path(directory.get_path()))
    menu.append(term_item)

    # menu.append(Gtk.SeparatorMenuItem.new())


main_menu = Gtk.Menu.new()

# // this prevents the menu from disappearing immediately,
# // since a GTK popup menu will disappear if the mouse is released while
# // the cursor sprite is not over the menu
# // (which can happen b/c the menu is forbidden from appearing
# // on the panel)
# this.just_clicked = false
# // so, if menu would be hidden when it was "just clicked",
# // nevermind that and show it anyway
def h(_):
    destroy_all_children_later(main_menu)
    Gtk.main_quit()

main_menu.connect("hide", h)

starting_uri = "file:///home/francesco"

populate_menu_with_directory_2(main_menu, starting_uri)
print("populated")
main_menu.show_all()
print("shown")


USE_JUST_POPUP = False

if USE_JUST_POPUP:
    # main_menu.popup(main_menu, None, None, None, 0, Gtk.get_current_event_time())
    main_menu.popup(None, None, None, None, 1, Gtk.get_current_event_time())
    print("done")

else:
    if not Gtk.Widget.get_realized(main_menu):
        main_menu.realize()
        toplevel = main_menu.get_toplevel()
        context = toplevel.get_style_context()

        context.remove_class("csd")
        context.add_class("xapp-status-icon-menu-window")

    # sintesi!

    display = Gdk.Display.get_default()
    seat = display.get_default_seat()
    pointer = seat.get_pointer()

    screen, posx, posy = pointer.get_position()

    attributes = Gdk.WindowAttr()
    attributes.window_type = Gdk.WindowType.CHILD
    attributes.x = posx
    attributes.y = posy
    attributes.width = 16
    attributes.height = 16

    attributes_mask = Gdk.WindowAttributesType.X | Gdk.WindowAttributesType.Y

    window = Gdk.Window.new(None, attributes, attributes_mask)

    win_rect = Gdk.Rectangle()
    win_rect.x = 0
    win_rect.y = 0
    win_rect.width = 16
    win_rect.height = 16

    event = Gdk.Event.new(Gdk.EventType.BUTTON_PRESS)
    event.any.window = window
    event.button.device = pointer

    # print(event)
    # print(event.any)
    # print(event.button)

    # sintesi fatta!

    main_menu.rect_window = window   # invece di set_data, facciamo direttamente così nel binding Python
    main_menu.window = window
    main_menu.anchor_hints = Gdk.AnchorHints.SLIDE_X | Gdk.AnchorHints.SLIDE_Y | Gdk.AnchorHints.RESIZE_X | Gdk.AnchorHints.RESIZE_Y

    main_menu.popup_at_rect(
        window,
        win_rect,
        Gdk.Gravity.NORTH_WEST,
        Gdk.Gravity.SOUTH_WEST,
        event
    )

    print("end")

    # QUESTO POTREBBE ESSERE MOLTO MOLTO IMPORTANTE
    Gtk.main()
    # invece, per il posizionamento fatto bene, questo può essere utile:
    # https://github.com/linuxmint/cinnamon/blob/master/files/usr/share/cinnamon/applets/xapp-status%40cinnamon.org/applet.js#L293

    window.destroy()
    event.free()

    print("freed")