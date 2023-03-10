from fastapi import Body, FastAPI, status
from fastapi.responses import JSONResponse, Response
from enum import Enum
from typing import List
from pydantic import BaseModel

app=FastAPI()

class PollOption(BaseModel):
  id: int
  name: str
  votes: int

class Poll(BaseModel):
  id: int
  name: str
  options: List[PollOption] = []

polls: List[Poll] = [
  {
    "id": 1,
    "name": "Poll 1",
    "options": [
      {
        "id": 1,
        "name": "Option 1",
        "votes": 0
      },
      {
        "id": 2,
        "name": "Option 2",
        "votes": 0
      }
    ]
  }
]

@app.get("/poll")
async def list_poll():
  return polls

@app.post("/poll")
async def create_poll(
  name: str = Body(default=None),
  options: List[str] = Body(default=None)
):
  next_id = max([poll["id"] for poll in polls]) + 1
  poll = {"id": next_id, "name": name, "options": []}
  opt_id = 1
  for option in options:
    poll["options"].append({
      "id": opt_id,
      "name": option,
      "votes": 0
    })
    opt_id += 1
  polls.append(poll)
  return JSONResponse(status_code=201, content=poll)

@app.get("/poll/{poll_id}")
async def get_poll(poll_id: int):
  poll = [poll for poll in polls if poll["id"] == poll_id]
  if len(poll) != 1:
    return Response(status_code=404)
  return poll[0]

@app.put("/poll/{poll_id}")
async def update_poll(poll_id: int, name: str = Body(default=None)):
  poll = [poll for poll in polls if poll["id"] == poll_id]
  if len(poll) != 1:
    return Response(status_code=404)

  poll = poll[0]
  polls.remove(poll)
  poll["name"] = name
  polls.append(poll)
  return JSONResponse(status_code=200, content=poll)

@app.delete("/poll/{poll_id}")
async def update_poll(poll_id: int):
  poll = [poll for poll in polls if poll["id"] == poll_id]
  if len(poll) != 1:
    return Response(status_code=404)
  polls.remove(poll[0])
  return Response(status_code=200)

@app.get("/poll/{poll_id}/vote")
async def create_item(poll_id: int):
  poll = [poll for poll in polls if poll["id"] == poll_id]
  if len(poll) != 1:
    return Response(status_code=404)
  return poll[0]["options"]

@app.post("/poll/{poll_id}/vote")
async def create_poll(
  poll_id: int,
  option: str = Body(default=None)
):
  poll = [poll for poll in polls if poll["id"] == poll_id]
  if len(poll) != 1:
    return Response(status_code=404)

  poll = poll[0]
  next_opt_id = max([opt["id"] for opt in poll["options"]]) + 1
  poll["options"].append({
    "id": next_opt_id,
    "name": option,
    "votes": 0
  })
  return poll

@app.get("/poll/{poll_id}/vote/{option_id}")
async def update_poll(poll_id: int, option_id: int):
  poll = [poll for poll in polls if poll["id"] == poll_id]
  if len(poll) != 1:
    return Response(status_code=404)

  poll = poll[0]
  option = [opt for opt in poll["options"] if opt["id"] == option_id]
  if len(option) != 1:
    return Response(status_code=404)
  return option[0]
 
@app.put("/poll/{poll_id}/vote/{option_id}")
async def update_poll(poll_id: int, option_id: int):
  poll = [poll for poll in polls if poll["id"] == poll_id]
  if len(poll) != 1:
    return Response(status_code=404)

  poll = poll[0]
  option = [opt for opt in poll["options"] if opt["id"] == option_id]
  if len(option) != 1:
    return Response(status_code=404)

  option = option[0]
  poll["options"].remove(option)
  option["votes"] += 1
  poll["options"].append(option)
  return JSONResponse(status_code=200, content=poll)

@app.delete("/poll/{poll_id}/vote/{option_id}")
async def update_poll(poll_id: int, option_id: int):
  poll = [poll for poll in polls if poll["id"] == poll_id]
  if len(poll) != 1:
    return Response(status_code=404)

  poll = poll[0]
  option = [opt for opt in poll["options"] if opt["id"] == option_id]
  if len(option) != 1:
    return Response(status_code=404)

  option = option[0]
  poll["options"].remove(option)
  option["votes"] = max(0, option["votes"] - 1)
  poll["options"].append(option)
  return JSONResponse(status_code=200, content=poll)

