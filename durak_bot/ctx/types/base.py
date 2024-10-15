from dataclasses import dataclass, fields, MISSING


@dataclass
class BaseState:
    def reset(self) -> None:
        for field in fields(self):
            if field.default_factory is not MISSING:
                setattr(self, field.name, field.default_factory())
                continue

            setattr(self, field.name, field.default)
