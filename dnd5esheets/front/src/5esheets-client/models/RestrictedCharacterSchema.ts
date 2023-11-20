/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { PartySchema } from './PartySchema';

/**
 * The details of a character, excluding the player
 */
export type RestrictedCharacterSchema = {
    id: number;
    name: string;
    slug: string;
    level?: (number | null);
    party: PartySchema;
};

