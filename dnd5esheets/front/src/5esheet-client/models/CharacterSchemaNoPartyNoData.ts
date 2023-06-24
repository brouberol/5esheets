/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { PartySchema } from "./PartySchema";
import type { PlayerSchema } from "./PlayerSchema";

/**
 * The details of a character, excluding the party
 */
export type CharacterSchemaNoPartyNoData = {
  id: number;
  name: string;
  slug: string;
  class_: string;
  level: number;
  data: Record<string, any>;
  party: PartySchema;
  player: PlayerSchema;
};
