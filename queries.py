
dbox_hist = '''SELECT sender, sender_name, receiver, receiver_name, ib.itemid, ib.sortname as name, quantity
FROM delivery_box_log dbl JOIN item_basic ib ON ib.itemid = dbl.itemid {where} ORDER BY date DESC LIMIT {limit}'''