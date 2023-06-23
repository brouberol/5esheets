/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { PartySchema } from './PartySchema';
import type { PlayerSchema } from './PlayerSchema';

/**
 * The details of a character, excluding the player
 */
export type CharacterSchemaNoPlayer = {
    id: number;
    name: string;
    slug: string;
    class_: string;
    level: number;
    /**
     * The embdedded character sheet JSON data
     */
    data: Record<string, any>;
    party: PartySchema;
    player: PlayerSchema;
};

