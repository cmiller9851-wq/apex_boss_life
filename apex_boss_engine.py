import hashlib
import logging
from dataclasses import dataclass
from typing import Dict

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('apex_boss_life')

@dataclass(frozen=True)
class StateRecord:
    source: str
    payload_hash: str
    version: int

class ApexBossEngine:
    """Production-grade state controller for apex_boss_life."""
    def __init__(self, node_id: str, baseline_hash: str):
        self.node_id = node_id
        self._baseline = baseline_hash
        self._records: Dict[str, StateRecord] = {}
        self._locked = False

    def ingest_state(self, source: str, payload: str, version: int) -> str:
        if self._locked:
            raise RuntimeError('engine locked')
        payload_hash = hashlib.sha256(payload.encode()).hexdigest()
        if payload_hash != self._baseline:
            self._locked = True
            logger.critical('integrity violation on %s', self.node_id)
            raise ValueError('baseline mismatch')
        rec = StateRecord(source=source, payload_hash=payload_hash, version=version)
        tx_id = hashlib.sha256(f'{source}:{payload_hash}:{version}'.encode()).hexdigest()
        self._records[tx_id] = rec
        logger.info('accepted state %s', tx_id)
        return tx_id

    def status(self) -> dict:
        return {
            'node_id': self.node_id,
            'locked': self._locked,
            'records': len(self._records)
        }

if __name__ == '__main__':
    engine = ApexBossEngine('APEX_ROOT', 'B45F...')
    print(engine.status())
