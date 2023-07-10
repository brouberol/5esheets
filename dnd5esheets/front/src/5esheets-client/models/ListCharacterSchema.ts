/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { PartySchema } from './PartySchema';
import type { PlayerSchema } from './PlayerSchema';

export type ListCharacterSchema = {
    id: number;
    name: string;
    slug: string;
    class_: string;
    level: number;
    player: PlayerSchema;
    party: PartySchema;
};

