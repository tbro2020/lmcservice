DB=db.sqlite3
TABLE="service_operation"

INDEXES="$(echo "SELECT name FROM sqlite_master WHERE type == 'index' AND tbl_name = '$TABLE';" | sqlite3 $DB)"
for i in $INDEXES; do
  echo "DROP INDEX '$i';" | sqlite3 $DB
done