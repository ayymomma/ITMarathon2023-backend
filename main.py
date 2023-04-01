import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Controller.InvitationController import invitation
from Controller.ProfileController import profile
from Controller.TimeController import time
from Controller.UserController import user

app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user, prefix="/api/user")
app.include_router(profile, prefix="/api/profile")
app.include_router(time, prefix="/api/time")
app.include_router(invitation, prefix="/api/invitation")


if __name__ == "__main__":
    config = uvicorn.Config("main:app", host="0.0.0.0", port=5051, log_level="info")
    server = uvicorn.Server(config)
    server.run()
