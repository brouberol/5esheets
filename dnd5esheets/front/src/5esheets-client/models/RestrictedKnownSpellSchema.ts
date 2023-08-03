/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { RestrictedSpellSchema } from './RestrictedSpellSchema';

/**
 * The details of a known spell (the association between a character and a spell)
 */
export type RestrictedKnownSpellSchema = {
    prepared: boolean;
    spell: RestrictedSpellSchema;
};

