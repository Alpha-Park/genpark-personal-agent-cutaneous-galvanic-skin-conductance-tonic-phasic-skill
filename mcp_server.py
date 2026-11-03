"""
MCP Server for Galvanic Skin Conductance (EDA/GSR) Tonic & Phasic Skill.
Conforms to Model Context Protocol (MCP) JSON-RPC 2.0 stdio specification.
"""

import sys
import json
from client import GalvanicSkinConductanceClient


def handle_request(line: str) -> None:
    try:
        req = json.loads(line)
    except Exception:
        return

    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-cutaneous-galvanic-skin-conductance-tonic-phasic-skill",
                    "version": "1.0.0"
                }
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/list":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "decompose_eda",
                        "description": "Decompose skin conductance series into tonic SCL and phasic SCR peaks to quantify sympathetic arousal.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "conductance_series_us": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Continuous skin conductance samples in microSiemens (uS)."
                                },
                                "sampling_rate_hz": {"type": "number", "description": "Sampling rate in Hz (default: 10.0)."},
                                "scr_threshold_us": {"type": "number", "description": "SCR peak threshold in uS (default: 0.05)."}
                            },
                            "required": ["conductance_series_us"]
                        }
                    }
                ]
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "decompose_eda":
            sampling_rate_hz = float(args.get("sampling_rate_hz", 10.0))
            scr_threshold_us = float(args.get("scr_threshold_us", 0.05))
            series = args.get("conductance_series_us", [])
            client = GalvanicSkinConductanceClient(sampling_rate_hz=sampling_rate_hz)
            try:
                res = client.decompose_eda(
                    conductance_series_us=[float(x) for x in series],
                    scr_threshold_us=scr_threshold_us
                )
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    }
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
    else:
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method {method} not found"}
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


def main():
    for line in sys.stdin:
        if line.strip():
            handle_request(line)


if __name__ == "__main__":
    main()
