healthcare:   uvicorn healthcare_agent.app:a2a_app   --host 0.0.0.0 --port 8001 --log-level info
general:      uvicorn general_agent.app:a2a_app      --host 0.0.0.0 --port 8002 --log-level info
orchestrator: uvicorn orchestrator.app:a2a_app        --host 0.0.0.0 --port 8003 --log-level info
treatment:    uvicorn treatment_agent.app:a2a_app --host 0.0.0.0 --port 8005 --log-level info
scheduling:    uvicorn scheduling_agent.app:a2a_app --host 0.0.0.0 --port 8006 --log-level info
cost: uvicorn cost_agent.app:a2a_app --host 0.0.0.0 --port 8008 --log-level info