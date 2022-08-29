for app in employees inventory objects procedures purchases users
do
    python3 manage.py dumpdata $app --format json --indent 2 > $app/fixtures/fixtures.json 
done