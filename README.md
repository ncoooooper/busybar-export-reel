# Export Reel

Follow an FFmpeg export by its real progress and estimate the seconds left.

Move progress off the editing screen. The bar reads the file FFmpeg already writes and uses actual render speed for the time estimate, so you can keep working in another application.

## Check the render and its ETA

1. Add `-progress /path/to/render.progress` to the export command and set the same filename in the companion.
2. Enter the expected output duration in seconds. While the job is running, **EXPORT** shows the fraction of the timeline encoded.
3. Turn the wheel to **ETA** to see the estimated seconds remaining. The recorded two-second job had finished, so the result was zero.

![The completed export reads 100% and its ETA reads 0s.](media/guide/inspect-render-eta.gif)

## Verify that the export finished

1. Turn back to the percentage page. The rear includes the reported frame and encoding speed.
2. If the job is still writing a block, wait for a complete progress block before comparing the next reading.
3. At `progress=end`, the bar reports 100% and zero seconds remaining. Open the output file in your editor if you also need to verify its contents.

![Zero seconds remaining returns to the completed export at 100%.](media/guide/return-to-export-percent.gif)

## Example from the emulator

A 180-second timeline with 120 seconds encoded has 60 seconds of media left. If FFmpeg reports 2× speed, the estimated wall-clock time is about 30 seconds. An unavailable speed leaves the running ETA blank. A real FFmpeg job generated its machine-readable progress file on this Mac.

## Set up the source

Start FFmpeg with -progress /path/to/render.progress and your normal input and output options. Set file to that progress path and duration_seconds to the target timeline length. The decoder uses the last complete progress block and handles unavailable speed and the terminal end marker.

## Connect the bar

Copy companion/example.json to a private config.json and adjust it for your source. From the project folder run `python3 companion/serve.py --config config.json`. Use Python 3.10+. Set Local companion URL to `http://127.0.0.1:8770/reading` on the emulator and allow local port 8770. On hardware, bind the companion to a trusted LAN interface and set its reachable address. The wheel browses pages. Click refreshes. Start pins or unpins the current page. The last good reading is labeled offline after a source error.

## Run in the emulator

Open BUSY Bar Emulator. From this repository, run:

```sh
~/.busy-emulator/bin/busy-emulator dev --once
```

Press **Back** to exit.

The GIFs are excerpts from the emulator recording. Each front-display pixel is shown at 9× its original width and height. The end frames pause for reading.

[Full recording](media/controls.mp4) · [Rear display](screenshots/back-1.png) · [Firmware test](EMULATOR-QA.md) · [MIT license](LICENSE)
