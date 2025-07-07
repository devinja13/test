import React from 'react';
interface IStepContext {
    completed: boolean;
    active: boolean;
    disabled: boolean;
    index: number;
    stepSize?: React.ReactText;
}
declare const StepContext: React.Context<IStepContext>;
export default StepContext;
