import { SpectralFeatures } from "./daap-features";
import { SimpleWDParam, WDParam } from "./wd-settings";

export class WDResult {
    baseFilename: string;
    videoFilename: string;
    // hsFrames: Array<string>;
    paramSummary: Array<WDParam>;
    daapFeatures: SpectralFeatures;
    plotVersionIndex: number = 0;
    compare: boolean = false;
    showVideo: boolean = false;

    constructor(baseFilename: string, videoFileName: string, summary: Array<WDParam>, daapFeatures: SpectralFeatures) {
        this.baseFilename = baseFilename;
        this.videoFilename = videoFileName;
        // this.hsFrames = hsFrames;
        this.paramSummary = summary;
        this.daapFeatures = daapFeatures;
    }
}