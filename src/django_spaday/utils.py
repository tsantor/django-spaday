def permissions_as_combobox(qs, grouped=True):
    """Return permissions for use in a v-combobox."""
    app_label = None
    vue_combobox_list = []
    for p in qs.select_related("content_type"):
        if grouped and app_label != p.content_type.app_label:
            app_label = p.content_type.app_label
            # model_label = p.content_type.model
            vue_combobox_list.extend(
                ({"header": f"{app_label.title()}"}, {"divider": True})
            )
        vue_combobox_list.append({"value": p.id, "text": p.name})
    return vue_combobox_list
