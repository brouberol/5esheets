/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { PlayerSchema } from './PlayerSchema';

/**
 * The details of a character, excluding the party
 */
export type CharacterSchemaNoEmbeddedFields = {
    id: number;
    name: string;
    slug: string;
    level?: (number | null);
    player: PlayerSchema;
};

