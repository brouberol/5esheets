/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { EquippedItemSchema } from './EquippedItemSchema';
import type { PartySchema } from './PartySchema';
import type { RestrictedKnownSpellSchema } from './RestrictedKnownSpellSchema';

/**
 * The details of a character, excluding the player
 */
export type CharacterSchemaNoPlayer = {
    id: number;
    name: string;
    slug: string;
    class_: (string | null);
    level: (number | null);
    party: PartySchema;
    equipment: Array<EquippedItemSchema>;
    spellbook: Array<RestrictedKnownSpellSchema>;
};

