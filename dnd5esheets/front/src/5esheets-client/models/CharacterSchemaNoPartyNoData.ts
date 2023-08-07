/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { EquippedItemSchema } from './EquippedItemSchema';
import type { PlayerSchema } from './PlayerSchema';
import type { RestrictedKnownSpellSchema } from './RestrictedKnownSpellSchema';

/**
 * The details of a character, excluding the party
 */
export type CharacterSchemaNoPartyNoData = {
    id: number;
    name: string;
    slug: string;
    class_: (string | null);
    level: (number | null);
    player: PlayerSchema;
    equipment: Array<EquippedItemSchema>;
    spellbook: Array<RestrictedKnownSpellSchema>;
};

