echo "Testing app APIs"
echo "Test 1: Creating Post"
curl -X POST localhost:8000/posts -d '{"title":"Debugging time","duration":2}' -H 'Content-Type: application/json' | jq
echo "Test 2: Read tables"
curl localhost:8000/posts | jq
echo "Test 3: Updating Post"
curl -X  curl -X PATCH localhost:8000/posts/4 -d '{"title":"Debugging Deployment Script","content":"Deployment script has bugs.","duration":3}' -H 'Content-Type: application/json' | jq
echo "Test 3: Read Specific Post"
curl localhost:8000/posts/15 | jq
echo "Test 4: Delete Post"
curl -X DELETE  localhost:8000/posts/1
curl localhost:8000/posts | jq

echo "Test 5: Creating User"
curl -X POST localhost:8000/users -d '{"email":"stacy@thing.com","password":"some123"}' -H 'Content-Type: application/json' | jq