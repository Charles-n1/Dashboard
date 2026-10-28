#!/usr/bin/env bash

read -p "Are you sure you want to update the table? (y/n) " answer

if [[ "$answer" == "n" ]]; then
    echo "Update cancelled."
    exit 1
fi

if [[ -f "code/database/dashboard.sql" ]]; then
    echo "File exists"
else
    echo "File does not exist"
    exit 1
fi

sudo docker exec -i dashboard_postgres pg_dump -U dashing -d dashboard > code/database/dashboard.temp.sql
sudo docker exec -i dashboard_postgres psql -U dashing -d dashboard -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
sudo docker exec -i dashboard_postgres psql -U dashing -d dashboard < code/database/dashboard.sql   

echo "Table updated successfully."	

exit 0