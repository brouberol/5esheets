/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ActionType } from './ActionType';
import type { SpellOrigin } from './SpellOrigin';

export type Spell = {
    name: string;
    description: string;
    prepared?: boolean;
    somatic?: boolean;
    verbal?: boolean;
    material?: boolean;
    ritual?: boolean;
    concentration?: boolean;
    invocation?: ActionType;
    origin?: SpellOrigin;
};

