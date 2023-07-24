/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { CharacterSheet } from './CharacterSheet';
import type { EquippedItemSchema } from './EquippedItemSchema';
import type { PartySchema } from './PartySchema';
import type { PlayerSchema } from './PlayerSchema';

/**
 * All details associated with a character
 */
export type CharacterSchema = {
    id: number;
    name: string;
    slug: string;
    class_?: (string | null);
    level?: (number | null);
    /**
     * The embdedded character sheet JSON data
     */
    data?: (CharacterSheet | null);
    party: PartySchema;
    player: PlayerSchema;
    equipment: Array<EquippedItemSchema>;
};

