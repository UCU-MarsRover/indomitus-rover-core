- **[Project Root]**
    - MR_00 (Mars Rover Main Assembly)

    - **[Folder] rover-frame**
        - MR_FRM_00 (Rover Frame Assembly)

    - **[Folder] suspension-system**
        - MR_SUS_00 (Suspension System Assembly)

    - **[Folder] container**
        - MR_CNT_00 (Container System Assembly)

    - **[Folder] robotic-arm** 
        - MR_ARM_00 (Robotic Arm Assembly)

        - **[Folder] arm-structure** 
            - MR_ARM_ATT_00 (Arm-to-Rover Attachment)
                - MR_ARM_ATT_01 (Drop-in Housing)
                - [Link] MR_COT_BRG_01 (Attachment Bearing)
                - [Link] MR_COT_CTR_01 (Arm Controller -- Raspberry Pi)
                - [Link] MR_COT_MTR_02 (High-Torque Motor)

            - MR_ARM_BAS_00 (Rotating Base Assembly)
                - MR_ARM_BAS_01 (Base Tube Mount)
                - MR_ARM_BAS_02 (Shoulder Motor L-Bracket)
                - [Link] MR_COT_TUB_01 (Base Tube)
                - [Link] MR_COT_OTR_01 (Clamp for Base Tube)
                - [Link] MR_COT_MTR_02 (High-Torque Motor)

            - MR_ARM_BDY_00 (Articulated Arm Body Assembly)
                - MR_ARM_BDY_01 (Static High-Torque Motor Mount)
                - MR_ARM_BDY_02 (Rotating High-Torque Motor Mount x2)
                - MR_ARM_BDY_03 (Forearm to Wrist Adapter)
                - MR_ARM_BDY_04 (Yaw to Pitch Wrist Adapter)
                - MR_ARM_BDY_05 (Pitch to Roll Wrist Adapter)
                - MR_ARM_BDY_06 (End-effector Motor Mount)
                - [Link] MR_COT_TUB_02 (Bicep Tube 400 mm)
                - [Link] MR_COT_TUB_03 (Forearm Tube 300 mm)
                - [Link] MR_COT_MTR_02 (High-Torque Motor)
                - [Link] MR_COT_MTR_03 (Low-Torque Motor x3)
                - [Link] MR_COT_MTR_04 (End-effector Motor)

        - **[Folder] end-effectors**
            - MR_ARM_SHR_00 (Shared End-Effector Components Assembly)
                - MR_ARM_SHR_01 (Housing)
                - MR_ARM_SHR_02 (Worm Shaft)
                - MR_ARM_SHR_03 (Worm Gear x2)
                - MR_ARM_SHR_04 (Faceplate)
                - MR_ARM_SHR_05 (Inner Finger Link x2)
                - MR_ARM_SHR_06 (Outer Finger Link x2)
                - [Link] MR_COT_BRG_02 (Bearing BS 290 SKF)

            - MR_ARM_JAW_00 (Jaw End-Effector Assembly)
                - MR_ARM_JAW_01 (Finger to Load Sensor Mount x2)
                - MR_ARM_JAW_02 (Fingertip x2)
                - MR_ARM_JAW_03 (Rubber Pad x2)
                - [Link] MR_COT_SNS_01 (Load Sensor x2)
                - [Link] MR_ARM_SHR_00 (Shared End-Effector Components Assembly)

            - MR_ARM_SMP_00 (Sampling End-Effector Assembly)
                - MR_ARM_SMP_01 (Shell x2)
                - MR_ARM_SMP_02_00 (Drill Assembly)
                    - MR_ARM_SMP_02_01 (Drill)
                    - MR_ARM_SMP_02_02 (Drill Motor Fixation)
                    - MR_ARM_SMP_02_03 (Drill Outer Tube)
                    - [Link] MR_COT_MTR_05 (Drill Motor)
                - [Link] MR_ARM_SHR_00 (Shared End-Effector Components Assembly)

            - MR_ARM_PMP_00 (Pump End-Effector Assembly)
                - MR_ARM_PMP_01 (Pump Flask Mount)
                - MR_ARM_PMP_02 (Flask)
                - MR_ARM_PMP_03 (Pump Outer Tube)
                - MR_ARM_PMP_04 (Pump Inner Tube)
                - [Link] MR_COT_SNS_02 (Moisture Sensor)
                - [Link] MR_COT_SNS_03 (pH sensor)
                - [Link] MR_COT_MTR_06 (Pump Motor)

    
    - **[Folder] COTs**
        - MR_COT_MTR_01 (Drive Motor -- DAMIAO DM-J10010L-2EC)
        - MR_COT_MTR_02 (High-Torque Motor -- SteadyWin8115-36)
        - MR_COT_MTR_03 (Low-Torque Motor -- DAMIAO DM-J4340-2EC)
        - MR_COT_MTR_04 (End-effector Motor -- Nema 17)
        - MR_COT_MTR_05 (Drill Motor -- 25GA370-226x1)
        - MR_COT_MTR_06 (Pump Motor -- DIMINUS DC MINI Air Pump)
        - MR_COT_BRG_01 (Attachment Bearing)
        - MR_COT_BRG_02 (Bearing BS 290 SKF)
        - MR_COT_CTR_01 (Arm Controller -- Raspberry Pi)
        - MR_COT_TUB_01 (Base Tube)
        - MR_COT_TUB_02 (Bicep Tube 400 mm)
        - MR_COT_TUB_03 (Forearm Tube 300 mm)
        - MR_COT_OTR_01 (Clamp for Base Tube)
        - MR_COT_SNS_01 (Load Sensor)
        - MR_COT_SNS_02 (Moisture Sensor)
        - MR_COT_SNS_03 (pH sensor)
