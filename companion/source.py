"""Monitor FFmpeg's machine-readable progress file without parsing its console."""
import json
from pathlib import Path
from serve import page
INTERVAL=1
def progress(path):
    # The final complete block is authoritative even during a partially written next block.
    with Path(path).expanduser().open("rb") as f:
        f.seek(0,2);end=f.tell();f.seek(max(0,end-65536));lines=f.read().decode(errors="replace").splitlines()
    if end>65536:lines=lines[1:]
    last=None;block={}
    for line in lines:
        if "=" not in line:continue
        k,v=line.split("=",1);block[k.strip()]=v.strip()
        if k=="progress":last=block;block={}
    if last is None:raise ValueError("No complete progress block yet")
    us=float(last.get("out_time_us",last.get("out_time_ms","0")))
    raw=last.get("speed","").strip().rstrip("x")
    try:speed=float(raw)
    except ValueError:speed=0
    return max(0,us/1e6),speed,last.get("progress")=="end",last.get("frame","--")
def snapshot(o,m):
    seconds,speed,done,frame=progress(o["file"]);total=float(o["duration_seconds"])
    if total<=0:raise ValueError("Duration must be positive")
    fraction=1 if done else min(1,seconds/total);eta=0 if done else max(0,total-seconds)/speed if speed>0 else None
    return dict(state="Export complete" if done else "Rendering",key=str(done),alert=done,pages=[
        page("EXPORT",f"{fraction:.0%}",f"Frame {frame}",f"Speed {speed:.2f}x",fraction=fraction),
        page("ETA","--" if eta is None else str(round(eta))+"s",f"Encoded {seconds:.1f} s",f"Planned {total:g} s")])
