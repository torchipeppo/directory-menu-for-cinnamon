/**
 * Cinnamon applet that attempts to replicate the functionality of the "Directory Menu" plugin from Xfce.
 * Written fron scratch, not translating the code of said plugin, as the author's first experiment in Cinnamon development.
 * 
 * "Cassettone" is Italian for "big drawer", and the nickname I used to give to the Directory Menu
 * since it had a drawer icon when I first saw it.
 * The applet is called by this codename in the code, instead of "Directory Menu" directly,
 * since a "Menu" is an already existing concept here, i.e. a dropwown menu object.
 */

const Applet = imports.ui.applet;
const Util = imports.misc.util;
const Gtk = imports.gi.Gtk;
const Gio = imports.gi.Gio;


class CassettoneApplet extends Applet.IconApplet{

    constructor(orientation, panel_height, instance_id) {
        super(orientation, panel_height, instance_id);

        this.set_applet_icon_symbolic_name("folder-symbolic");
        this.set_applet_tooltip(_("Directory Menu"));

        this.menu = Gtk.Menu.new();

        // TODO this should be a setting
        let startingDirectory = Gio.File.new_for_path("/home/francesco/Universita");

        this.populate_menu_with_directory(startingDirectory, this.menu);



        // TEST
        this.menu.append(Gtk.SeparatorMenuItem.new());
        let subMenuItem = Gtk.ImageMenuItem.new_with_label("PIPPO");
        let subMenu = Gtk.Menu.new();
        subMenu.append(Gtk.ImageMenuItem.new_with_label("pippo"));
        subMenu.append(Gtk.ImageMenuItem.new_with_label("pippopippo"));
        subMenuItem.set_submenu(subMenu);
        this.menu.append(subMenuItem);
        subMenu.connect("show", () => {
            subMenu.append(Gtk.ImageMenuItem.new_with_label("zan zan zan"));
            subMenuItem.show_all();
        });
        subMenu.connect("hide", () => {
            subMenu.append(Gtk.ImageMenuItem.new_with_label("..."));
            subMenuItem.show_all();
        });
    }

    populate_menu_with_directory(directory, menu) {
        const iter = directory.enumerate_children('standard::*', Gio.FileQueryInfoFlags.NONE, null);

        let dirs = [];
        let nondirs = [];

        var info = iter.next_file(null);
        while (info != null) {
            // TODO skip hidden files as a setting (there should be info.get_is_hidden(), check doc)
            info.display_name = info.get_display_name();
            info.content_type = info.get_content_type();
            if (info.get_content_type() == "inode/directory") {
                dirs.push(info);
            }
            else {
                nondirs.push(info);
            }
            var info = iter.next_file(null);
        }

        dirs.sort((a,b) => strcmp_insensitive(a.display_name, b.display_name));
        nondirs.sort((a,b) => strcmp_insensitive(a.display_name, b.display_name));

        dirs.forEach(info => this.add_to_menu_from_gioinfo(info, menu));
        nondirs.forEach(info => this.add_to_menu_from_gioinfo(info, menu));
    }

    add_to_menu_from_gioinfo(info, menu) {
        let display_text = info.display_name;
        let icon = Gio.content_type_get_icon(info.content_type);
        let image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.MENU);
        let item = Gtk.ImageMenuItem.new_with_label(display_text);
        item.set_image(image);
        item.connect("activate", () => {
            Util.spawn(["nemo"]);
        });
        menu.append(item);
    }

    on_applet_clicked() {
        // gotta delay by a bit b/c the GTK menu will disappear on mouse release if the cursor sprite is not on the menu.
        // 75 ms is the min for a mouse, 175 ms for a touchpad.
        // TODO see if there's a GTK way to disable the release-disappearance for some time,
        //      or make the delay a setting
        sleep(175).then(()=>{
            this.menu.show_all();
            this.menu.popup(null, null, null, 0, Gtk.get_current_event_time());
        })
    }

}

function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
}

function strcmp_insensitive(a, b) {
    a = a.toLowerCase();
    b = b.toLowerCase();
    if (a < b) return -1;
    if (a > b) return 1;
    return 0;
}

function main(metadata, orientation, panel_height, instance_id) {
    return new CassettoneApplet(orientation, panel_height, instance_id);
}

