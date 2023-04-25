#pragma once

module Demo
{
    enum Operation {
        SUM,
        SUB,
        MAX,
        MIN
    };

    struct OpRequest {
        int a;
        int b;
        Operation operation;
    };

    struct OpResponse {
        int r;
    };
};