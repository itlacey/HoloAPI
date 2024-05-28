from pydantic import BaseModel

class LoveNote(BaseModel):
    message: str = "This is from the HoloAPI, and should be picked up!!!"
