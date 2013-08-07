#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create instances for Gruene NRW.

Run this script after creating the region hierarchy.

call it with:
LD_LIBRARY_PATH=parts/geos/lib bin/adhocpy src/adhocracy.gruene_nrw_theme/scripts/create-regional-instances.py etc/adhocracy.ini
"""

# boilerplate code. copy that
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'src/adhoracy'))
from scripts.common import create_parser, load_from_args
# /end boilerplate code

from sqlalchemy import not_
from sqlalchemy import or_

from adhocracy.model import meta
from adhocracy.model import Instance
from adhocracy.model import InstanceBadge
from adhocracy.model import Region
from adhocracy.model import User
from adhocracy.model import CategoryBadge
from adhocracy.model.instance import instance_table
from adhocracy.model.region import normalize_region_name


MAX_KEY_LENGTH = instance_table.columns.key.type.length

UPDATE_INSTANCES = False

DESCRIPTION = u"""
Willkommen beim %(label)s der Grünen NRW!
"""


def assign_instancebadge(instance, badge_title, color):
    ib = InstanceBadge.find(badge_title)
    if ib is None:
        ib = InstanceBadge.create(badge_title, color, True, u'')
    ib.assign(instance, User.find('admin'))


def create_municipality(region):

    def removePrefix(str, prefix):
        return str[len(prefix):] if str.startswith(prefix) else str

    def removeSuffix(str, suffix):
        return str[:-len(suffix)] if str.endswith(suffix) else str

    def normalize_label(label, region):

        # normalizing

        label = removePrefix(label, 'Kreis ')

        if label.startswith(u'Landkreis '):
            name = removePrefix(label, u'Landkreis ')

        if label.endswith(u', Stadt'):
            name = removeSuffix(label, u', Stadt')
            label = name

        return label

    def normalize_key(s):
        """ normalize_key creates a sensitive and nice subdomain url """
        key = normalize_region_name(s)

        if len(key) > MAX_KEY_LENGTH:
            print("stripping key %s with %d characters" % (key, len(key)))
            key = key[:MAX_KEY_LENGTH]
            key.rstrip(u'-')

        return key

    label = normalize_label(region.name, region)

    if region.admin_level == 4:
        label = u'LV %s' % label
    elif region.admin_level == 6:
        label = u'KV %s' % label
    elif region.admin_level == 8:
        label = u'OV %s' % label

    key = normalize_key(label)

    user = meta.Session.query(User).filter(User.user_name == u'admin').one()
    locale = 'de_DE'
    description = DESCRIPTION % {'label': label}

    q = meta.Session.query(Instance).filter(or_(
        Instance.key == key,
        Instance.region_id == region.id,
    ))

    if q.count() == 0:
        print("Creating instance %s from region %s" % (key, region.name))
        instance = Instance.create(key, label, user, description, locale)

    else:
        if UPDATE_INSTANCES:
            print("Updating instance %s / region %s" % (key, region.name))

            instance = q.one()

            for attr in ['key', 'label', 'locale', 'description']:

                new = eval(attr)
                old = getattr(instance, attr)

                if new != old:

                    if attr in ['key', 'label']:
                        print 'Updating %s from %s to %s' % (attr, old, new)

                    setattr(instance, attr, new)

        else:
            print("there is already an instance with key %s" % key)
            return

    fix_categories = {
    }

    current_categories = CategoryBadge.all(instance)

    for category in current_categories:
        if category.title in fix_categories.keys():

            category.description = fix_categories[category.title]
            del fix_categories[category.title]
        else:
            meta.Session.delete(category)

    for (title, description) in fix_categories.iteritems():
        CategoryBadge.create(title, '#a4a4a4', True, description,
                             instance=instance)

    instance.region = region

    instance.use_norms = False
    instance.milestones = False
    instance.allow_adopt = False
    instance.allow_delegate = False

    if region.admin_level == 4:
        assign_instancebadge(instance, 'Landesverband', '#9D4647')
    elif region.admin_level == 6:
        assign_instancebadge(instance, 'Kreisverband', '#ffed00')
    elif region.admin_level == 8:
        assign_instancebadge(instance, 'Ortsverband', '#429f31')


def main():
    parser = create_parser(description=__doc__)
    args = parser.parse_args()
    load_from_args(args)

    a4_query = meta.Session.query(Region).filter(Region.admin_level == 4)

    a6_query = meta.Session.query(Region).filter(Region.admin_level == 6)\
        .join(Region.outer_regions, aliased=True)\
        .filter(Region.admin_level == 4)\

    a8_query = meta.Session.query(Region).filter(Region.admin_level == 8)\
        .join(Region.outer_regions, aliased=True)\
        .filter(Region.admin_level == 4)\

    for region in a4_query.union(a6_query.union(a8_query)).all():

        try:
            create_municipality(region)
        except Exception, e:
            print("couldn't create instance for region %s, because of %s" %
                  (region.name, e))

    meta.Session.commit()

if __name__ == '__main__':
    sys.exit(main())
