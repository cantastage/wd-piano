import { SimpleWDParam } from "./wd-settings";

export class WDResult {
    videoFileName:string;
    paramSummary: Array<SimpleWDParam>;
    daapFeatures: []; // TODO assign type once implemented

    constructor(videoFileName:string, summary: Array<SimpleWDParam>, daapFeatures: []) {
        this.videoFileName = videoFileName;
        this.paramSummary = summary;
        this.daapFeatures = daapFeatures;
    }
}