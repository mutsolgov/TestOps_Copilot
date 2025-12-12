export enum TestType {
    UI = "ui",
    API = "api"
}

export interface GenerationRequest {
    feature_description: string;
    test_type: TestType;
    owner: string;
    priority: string;
    is_manual: boolean;
}

export interface TestCase {
    title: string;
    description: string;
    steps: any[];
    code: string;
    tags: string[];
}
