# Beschluss -> Entwurf

# Sometimes it is not easy to decide. In those cases we should
# replace the string with `CHECK/possibility1/.../` so we can
# decide manually.

sed -i de/LC_MESSAGES/adhocracy.po \
-e 's/Beschluss/Entwurf/g'
