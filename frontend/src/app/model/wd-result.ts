import { DAAPFeatures } from "./daap-features";
import { SimpleWDParam, WDParam } from "./wd-settings";

export class WDResult {
    videoFilename:string;
    paramSummary: Array<WDParam>;
    daapFeatures: DAAPFeatures; // TODO assign type once implemented
    // summary: Array<WDParam>;

    constructor(videoFileName:string, summary: Array<WDParam>, daapFeatures: DAAPFeatures) {
        this.videoFilename = videoFileName;
        this.paramSummary = summary;
        this.daapFeatures = daapFeatures;
        // this.summary = new Array<WDParam>();
    }

    
}