echo "Testing app APIs"
echo "Test 1: Creating Event"
curl -X POST localhost:8000/events -d '{"title":"Debugging time","duration":2}' -H 'Content-Type: application/json' | jq
echo "Test 2: Read tables"
curl localhost:8000/events | jq
echo "Test 3: Updating Event"
curl -X  curl -X PATCH localhost:8000/events/4 -d '{"title":"Debugging Deployment Script","description":"Deployment script has bugs.","duration":3}' -H 'Content-Type: application/json' | jq
echo "Test 3: Read Specific Event"
curl localhost:8000/events/15 | jq
echo "Test 4: Delete Event"
curl -X DELETE  localhost:8000/events/1
curl localhost:8000/events | jq

echo "Test 5: Creating User"
curl -X POST localhost:8000/users -d '{"email":"stacy@thing.com","password":"some123"}' -H 'Content-Type: application/json' | jq