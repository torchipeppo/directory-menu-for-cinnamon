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
        this.info = info;   // TODO should get passed a proper info

        // TEMP
        let icon = St.TextureCache.get_default().load_gicon(null, Gio.content_type_get_icon("inode/directory"), 24);

        // TEMP
        let display_text = info.text;

        this.box.add(icon);

        let label = new St.Label({ text: display_text, y_align: Clutter.ActorAlign.CENTER });

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

        let button = new CassettoneMenuItem({text: "PIPPO"});
        button.connect("activate", (button, event)=> {
            Util.spawn(["nemo"]);
            this.menu.toggle();
        })
        this.cassettoneBox.add_child(button.actor);
    }

    on_applet_clicked() {
        this.menu.toggle();
    }

}

function main(metadata, orientation, panel_height, instance_id) {
    return new CassettoneApplet(orientation, panel_height, instance_id);
}

