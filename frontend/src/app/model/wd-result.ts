import { SpectralFeatures } from "./daap-features";
import { SimpleWDParam, WDParam } from "./wd-settings";

export class WDResult {
    baseFilename: string;
    videoFilename:string;
    paramSummary: Array<WDParam>;
    daapFeatures: SpectralFeatures; // TODO assign type once implemented
    // summary: Array<WDParam>;

    constructor(baseFilename: string, videoFileName:string, summary: Array<WDParam>, daapFeatures: SpectralFeatures) {
        this.baseFilename = baseFilename;
        this.videoFilename = videoFileName;
        this.paramSummary = summary;
        this.daapFeatures = daapFeatures;
        // this.summary = new Array<WDParam>();
    }

    
}