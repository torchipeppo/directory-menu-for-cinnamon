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
const PopupMenu = imports.ui.popupMenu;
const St = imports.gi.St;
const Lang = imports.lang;
const Gtk = imports.gi.Gtk;
const Clutter = imports.gi.Clutter;
const Gio = imports.gi.Gio;


class CassettoneMenuItem extends PopupMenu.PopupBaseMenuItem {
    constructor(info, params) {
        super(params);
        this.box = new St.BoxLayout({ style_class: 'popup-combobox-item', style: 'padding: 0px;' });
        this.info = info;

        let icon = St.TextureCache.get_default().load_gicon(null, Gio.content_type_get_icon(info.content_type), 24);

        let display_text = info.display_name;
        let label = new St.Label({ text: display_text, y_align: Clutter.ActorAlign.CENTER });
        
        this.box.add(icon);
        this.box.add(label);
        this.addActor(this.box);
    }
};


class CassettoneApplet extends Applet.IconApplet{

    constructor(orientation, panel_height, instance_id) {
        super(orientation, panel_height, instance_id);

        this.set_applet_icon_symbolic_name("folder-symbolic");
        this.set_applet_tooltip(_("Directory Menu"));

        this.menuManager = new PopupMenu.PopupMenuManager(this);
        this.menu = new Applet.AppletPopupMenu(this, orientation);
        this.menuManager.addMenu(this.menu);

        this.mainContainer = new St.BoxLayout({ vertical: true });
        this.menu.addActor(this.mainContainer);

        this.cassettoneScrollBox = new St.ScrollView({ x_fill: true, y_fill: false, y_align: St.Align.START });
        this.cassettoneScrollBox.set_auto_scrolling(true);
        this.mainContainer.add(this.cassettoneScrollBox);

        this.cassettoneBox = new St.BoxLayout({ vertical:true });
        this.cassettoneScrollBox.add_actor(this.cassettoneBox);
        this.cassettoneScrollBox.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC);
        this.cassettoneScrollBox.add_style_class_name("vfade");

        // TODO this should be a setting
        let startingDirectory = Gio.File.new_for_path("/home/francesco/Universita");

        this.build_dropdown_for_directory(startingDirectory, this.cassettoneBox);
    }

    build_dropdown_for_directory(directory, box) {
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

        dirs.forEach(info => this.add_to_dropdown_from_gioinfo(info, box));
        nondirs.forEach(info => this.add_to_dropdown_from_gioinfo(info, box));
    }

    add_to_dropdown_from_gioinfo(info, box) {
        let button = new CassettoneMenuItem(info);
        button.connect("activate", (button, event) => {
            Util.spawn(["nemo"]);
            this.menu.toggle();
        })
        box.add_child(button.actor);
    }

    on_applet_clicked() {
        this.menu.toggle();
    }

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

