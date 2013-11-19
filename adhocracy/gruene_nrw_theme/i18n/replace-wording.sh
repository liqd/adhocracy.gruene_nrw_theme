# Beschluss -> Entwurf

# You may need to run this multiple times

# Sometimes it is not easy to decide. In those cases we should
# replace the string with `CHECK/possibility1/.../` so we can
# decide manually.

sed -i de/LC_MESSAGES/adhocracy.po \
-e 's/Elternbeschluss/Elternentwurf/g' \
-e 's/Beschlüsse/Entwürfe/g' \
-e 's/Beschluss/Entwurf/g' \
\
-e 's/Dieses Badge wird nicht genutzt. Es/Diese Plakette wird nicht genutzt. Sie/g' \
-e 's/\(msgstr.*\)Kein Miniaturbild-Badge/\1Keine Miniaturbild-Plakette/g' \
-e 's/\(msgstr.*\)Miniaturbildbadges/\1Miniaturbildplaketten/g' \
-e 's/\(msgstr.*\)Miniaturbildbadge/\1Miniaturbildplakette/g' \
-e 's/\(msgstr.*\)Nutzerbadges/\1Nutzerplaketten/g' \
-e 's/\(msgstr.*\)Nutzerbadge/\1Nutzerplakette/g' \
-e 's/\(msgstr.*\)Benutzerbadge/\1Nutzerplakette/g' \
-e 's/\(msgstr.*\)Gruppenbadge/\1Gruppenplakette/g' \
-e 's/\(msgstr.*\)Vorschlagsbadge/\1Vorschlagsplakette/g' \
-e 's/\(msgstr.*\)Badge-Auswahl/\1Plaketten-Auswahl/g' \
-e 's/\(msgstr.*\)Userbadge labels/\1Nutzerplaketten Namen/g' \
-e 's/\(msgstr.*\)des Badges/\1der Plakette/g' \
-e 's/\(msgstr.*\)Das Badge/\1Die Plakette/g' \
-e 's/\(msgstr.*\)das Badge/\1die Plakette/g' \
-e 's/\(msgstr.*\)den Badge/\1die Plakette/g' \
-e 's/\(msgstr.*\)iesem Badge/\1ieser Plakette/g' \
-e 's/\(msgstr.*\)ieses Badge/\1iese Plakette/g' \
-e 's/\(msgstr.*\)ieser Badge/\1ieser Plakette/g' \
-e 's/\(msgstr.*\)Badges/\1Plaketten/g' \
-e 's/\(msgstr.*\)Badge/\1Plakette/g' \
-e 's/\(msgstr.*\)badge/\1Plakette/g'
