-- ###
-- Copyright (c) 2018, Rice University
-- This software is subject to the provisions of the GNU Affero General
-- Public License version 3 (AGPLv3).
-- See LICENCE.txt for details.
-- ###

-- arguments: id:string
WITH RECURSIVE t(node, title, parent, path, value) AS (
      SELECT nodeid, coalesce(title,name), parent_id, ARRAY[nodeid], documentid
      FROM trees tr, modules m
      WHERE m.uuid = %(id)s::uuid
      AND tr.documentid = m.module_ident
      AND tr.parent_id IS NOT NULL
    UNION ALL
      SELECT c1.nodeid, c1.title, c1.parent_id,
             t.path || ARRAY[c1.nodeid], c1.documentid
              FROM trees c1
              JOIN t ON (c1.nodeid = t.parent)
              WHERE not nodeid = any (t.path)
        )


        SELECT name, module_version(major_version,minor_version) as ver, uuid, t.*
        from t join modules on t.value = module_ident
        where t.parent is NULL order by revised, major_version, minor_version limit 1;
