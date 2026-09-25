"""Serve the production web export with the real API on one local origin."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from fastapi.staticfiles import StaticFiles
from arccraft.service import app
import uvicorn
app.mount('/',StaticFiles(directory=ROOT/'out',html=True),name='web')
if __name__=='__main__':uvicorn.run(app,host='127.0.0.1',port=3000)
