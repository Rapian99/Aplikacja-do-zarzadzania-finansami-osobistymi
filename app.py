from loguru import logger


# ===================== [ Variables / constants ] =====================
PROGRAM_NAME = "Aplikacja do zarzadzania finansami osobistymi"

# ===================== [ Functions ] =====================


# ======================== [ Main ] =======================


@logger.catch
def main():
    logger.add(
        "./logs/{time:YYYY-MM-DD}.log",
        retention="1 week",
        compression="gz",
        level="TRACE",
        rotation="1h",
    )
    logger.success(f"Program {PROGRAM_NAME} started!")


if __name__ == "__main__":
    main()
