import { SimpleWDParam } from "./wd-settings";

export class WDResult {
    videoFileName:string;
    paramSummary: Array<SimpleWDParam>;
    daapFeatures: any; // TODO assign type once implemented

    constructor(videoFileName:string, summary: Array<SimpleWDParam>, daapFeatures: any) {
        this.videoFileName = videoFileName;
        this.paramSummary = summary;
        this.daapFeatures = daapFeatures;
    }
}