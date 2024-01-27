"""
KNOWN ISSUES

- The menu only appears if the mouse button is clicked and released
  within a short, but undetermined, fraction of a second.
  A slower click will cause this script to be executed correctly,
  but then hang up on Gtk.main without showing the menu, and without terminating.
  (This didn't happen in the GJS-only version, but then again, that version does nothing on Cinnamon 5.4+)

- Doesn't work by clicking with a touchpad. At least, not on the author's laptop.
  This is because clicking with a touchpad delays the press and release signals (may depend on laptop manufacturer),
  therefore resulting in the above known issue (including spawning a process that won't terminate)

- This applet's menu doesn't "lock up" the panel events (?) the way XApp Status Icons do (not yet, at least),
  so some counterintuitive but harmless behavior may be observed, such as the tooltip appearing beneath the menu,
  or an auto-hide panel disappearing while navigating the menu.

- A warning will be recorded on .xsession-errors if the menu is dismissed without clicking anything,
  because "no output" is not a valid json. This is harmless.

- Gtk.ImageMenuItem.new_with_label is seemingly deprecated. This is harmless.
"""

#!/usr/bin/python3

import os
import sys
import json

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("GLib", "2.0")
from gi.repository import Gio, Gtk, Gdk, GLib

def log(message):
    with open("/tmp/DM-remake-log.txt", "a") as f:
        f.write(str(message) + "\n")
    print(message, file=sys.stderr)





def populate_menu_with_directory(menu, directory_uri):
    directory = Gio.File.new_for_uri(directory_uri)
    # // First, the two directory actions: Open Folder and Open In Terminal

    temp_item = Gtk.MenuItem.new_with_label("Python Remake")
    temp_item.set_sensitive(False)
    menu.append(temp_item)

    open_item = Gtk.ImageMenuItem.new_with_label("Open Folder")
    open_image = Gtk.Image.new_from_icon_name("folder", Gtk.IconSize.MENU)
    open_item.set_image(open_image)
    open_item.connect("activate", lambda _: launch(directory.get_uri(), Gtk.get_current_event_time()))
    menu.append(open_item)

    term_item = Gtk.ImageMenuItem.new_with_label("Open in Terminal")
    term_image = Gtk.Image.new_from_icon_name("terminal", Gtk.IconSize.MENU)
    term_item.set_image(term_image)
    term_item.connect("activate", lambda _: open_terminal_at_path(directory.get_path()))
    menu.append(term_item)

    menu.append(Gtk.SeparatorMenuItem.new())

    # log(directory_uri)

    iter = directory.enumerate_children('standard::*', Gio.FileQueryInfoFlags.NONE, None)

    dirs = []
    nondirs = []

    info = iter.next_file(None)
    while info != None:
        if (not info.get_is_hidden() or show_hidden):     # // <-- skip hidden files
            info.display_name = info.get_display_name()
            info.content_type = info.get_content_type()
            info.file = directory.get_child_for_display_name(info.display_name)
            info.is_directory = (info.get_content_type() == "inode/directory")

            if (info.is_directory):
                dirs.append(info)
            else:
                nondirs.append(info)

        info = iter.next_file(None)

    dirs.sort(key = lambda info: info.display_name.lower())
    nondirs.sort(key = lambda info: info.display_name.lower())

    for info in dirs:
        add_to_menu_from_gioinfo(menu, info)
    for info in nondirs:
        add_to_menu_from_gioinfo(menu, info)

def add_to_menu_from_gioinfo(menu, info):
    display_text = info.display_name

    icon = Gio.content_type_get_icon(info.content_type)
    image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.MENU)

    uri = info.file.get_uri()

    item = Gtk.ImageMenuItem.new_with_label(display_text)
    item.set_image(image)

    if info.is_directory:
        subMenu = create_subdirectory_submenu(uri)
        item.set_submenu(subMenu)
    else:
        item.connect("activate", lambda _: launch(uri, Gtk.get_current_event_time()))

    menu.append(item)

def create_subdirectory_submenu(uri):
    subMenu = Gtk.Menu.new()

    def f(_):
        populate_menu_with_directory(subMenu, uri)
        subMenu.show_all()

    subMenu.connect("show", f)

    subMenu.connect("hide", lambda _: destroy_all_children_later(subMenu))

    return subMenu

def launch(uri, timestamp):
    print(json.dumps({
        "action": "launch_default_for_uri",
        "uri": uri,
        "timestamp": timestamp,
    }))

def open_terminal_at_path(path):
    print(json.dumps({
        "action": "open_terminal_at_path",
        "path": path,
    }))

def destroy_subitem_later(subItem):
    def g2():
        subItem.destroy()
        return False
    # // destroy at some future instant, but not right now so we have time for the activate event
    GLib.idle_add(priority=GLib.PRIORITY_HIGH_IDLE, function=g2)

def destroy_all_children_later(menu):
    menu.foreach(destroy_subitem_later)


# https://github.com/linuxmint/xapp/blob/master/libxapp/xapp-status-icon.c#L197
def synthesize_event(args):
    display = Gdk.Display.get_default()
    seat = display.get_default_seat()
    pointer = seat.get_pointer()

    # https://github.com/linuxmint/xapp/blob/master/libxapp/xapp-status-icon.c#L222
    # would be nice to determine it somehow, but it might not be so important right now
    PRIV_ICON_SIZE = 16

    # screen, posx, posy = pointer.get_position()
    # posx, posy = args["x"], args["y"]
    if args["orientation"] == int(Gtk.PositionType.TOP):
        posx = args["x"]
        posy = args["y"] - PRIV_ICON_SIZE;
        rect_anchor = Gdk.Gravity.SOUTH_WEST;
        menu_anchor = Gdk.Gravity.NORTH_WEST;
    elif args["orientation"] == int(Gtk.PositionType.LEFT):
        posx = args["x"] - PRIV_ICON_SIZE;
        posy = args["y"]
        rect_anchor = Gdk.Gravity.NORTH_EAST;
        menu_anchor = Gdk.Gravity.NORTH_WEST;
    elif args["orientation"] == int(Gtk.PositionType.RIGHT):
        posx = args["x"]
        posy = args["y"]
        rect_anchor = Gdk.Gravity.NORTH_WEST;
        menu_anchor = Gdk.Gravity.NORTH_EAST;
    else: # int(Gtk.PositionType.BOTTOM) is default
        posx = args["x"]
        posy = args["y"]
        rect_anchor = Gdk.Gravity.NORTH_WEST;
        menu_anchor = Gdk.Gravity.SOUTH_WEST;

    attributes = Gdk.WindowAttr()
    attributes.window_type = Gdk.WindowType.CHILD
    attributes.x = posx
    attributes.y = posy
    attributes.width = PRIV_ICON_SIZE
    attributes.height = PRIV_ICON_SIZE

    attributes_mask = Gdk.WindowAttributesType.X | Gdk.WindowAttributesType.Y

    window = Gdk.Window.new(None, attributes, attributes_mask)

    win_rect = Gdk.Rectangle()
    win_rect.x = 0
    win_rect.y = 0
    win_rect.width = PRIV_ICON_SIZE
    win_rect.height = PRIV_ICON_SIZE

    event = Gdk.Event.new(Gdk.EventType.BUTTON_PRESS)
    event.any.window = window
    event.button.device = pointer

    # log(event)
    # log(event.any)
    # log(event.button)

    return event, window, win_rect, rect_anchor, menu_anchor





main_menu = Gtk.Menu.new()

def on_main_menu_hidden(_):
    destroy_all_children_later(main_menu)
    Gtk.main_quit()

main_menu.connect("hide", on_main_menu_hidden)

args = json.loads(sys.argv[1])
starting_uri = args["starting_uri"]
show_hidden = args["show_hidden"]

populate_menu_with_directory(main_menu, starting_uri)

main_menu.show_all()

if not Gtk.Widget.get_realized(main_menu):
    main_menu.realize()
    toplevel = main_menu.get_toplevel()
    context = toplevel.get_style_context()

    context.remove_class("csd")
    context.add_class("xapp-status-icon-menu-window")


event, window, win_rect, rect_anchor, menu_anchor = synthesize_event(args)


main_menu.rect_window = window   # invece di set_data, facciamo direttamente così nel binding Python
main_menu.window = window
main_menu.anchor_hints = Gdk.AnchorHints.SLIDE_X | Gdk.AnchorHints.SLIDE_Y | Gdk.AnchorHints.RESIZE_X | Gdk.AnchorHints.RESIZE_Y

main_menu.popup_at_rect(
    window,
    win_rect,
    rect_anchor,
    menu_anchor,
    event
)

Gtk.main()
# this is a blocking call

window.destroy()
event.free()
