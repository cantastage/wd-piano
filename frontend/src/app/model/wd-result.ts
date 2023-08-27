import { DAAPFeatures } from "./daap-features";
import { SimpleWDParam } from "./wd-settings";

export class WDResult {
    videoFilename:string;
    paramSummary: Array<SimpleWDParam>;
    daapFeatures: DAAPFeatures; // TODO assign type once implemented

    constructor(videoFileName:string, summary: Array<SimpleWDParam>, daapFeatures: any) {
        this.videoFilename = videoFileName;
        this.paramSummary = summary;
        this.daapFeatures = daapFeatures;
    }

    
}