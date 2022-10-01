# temporal-analysis

## Repositories
| Name | Size | Last Version | Java Files | Source |
| --- | --- | --- | --- | --- |
| [mockito](https://github.com/mockito/mockito) | Very Large | 4.7.0 | 949 | [Maven Central](https://mvnrepository.com/artifact/org.mockito/mockito-core) |
| [spring-kafka](https://github.com/spring-projects/spring-kafka) | Large | 2.9.0 | 502 | [Maven Central](https://mvnrepository.com/artifact/org.springframework.kafka/spring-kafka) |
| [gson](https://github.com/google/gson) | Medium | 2.9.1 | 218 | [Maven Central](https://mvnrepository.com/artifact/com.google.code.gson/gson) |
| [java-jwt](https://github.com/auth0/java-jwt) | Small | 4.0.0 | 75 | [Maven Central](https://mvnrepository.com/artifact/com.auth0/java-jwt) |

## Graphs
- [Cumulative measures](#cumulative-measures)
    - [Averages java-jwt](#averages-java-jwt)
    - [Averages gson](#averages-gson)
    - [Averages spring-kafka](#averages-spring-kafka)
    - [Averages mockitoa](#averages-mockito)
    - [Maximums java-jwt](#maximums-java-jwt)
    - [Maximums gson](#maximums-gson)
    - [Maximums spring-kafka](#maximums-spring-kafka)
    - [Maximums mockito](#averages-mockito)
- [Thresholds](#thresholds)
    - [ABC Threshold java-jwt](#abc-threshold-java-jwt)
    - [ABC Threshold gson](#abc-threshold-gson)
    - [ABC Threshold spring-kafka](#abc-threshold-spring-kafka)
    - [ABC Threshold mockito](#abc-threshold-mockito)
    - [WMC Threshold java-jwt](#wmc-threshold-java-jwt)
    - [WMC Threshold gson](#wmc-threshold-gson)
    - [WMC Threshold spring-kafka](#wmc-threshold-spring-kafka)
    - [WMC Threshold mockito](#wmc-threshold-mockito)
    - [NPM Threshold java-jwt](#npm-threshold-java-jwt)
    - [NPM Threshold gson](#npm-threshold-gson)
    - [NPM Threshold spring-kafka](#npm-threshold-spring-kafka)
    - [NPM Threshold mockito](#npm-threshold-mockito)
    - [NPA Threshold java-jwt](#npa-threshold-java-jwt)
    - [NPA Threshold gson](#npa-threshold-gson)
    - [NPA Threshold spring-kafka](#npa-threshold-spring-kafka)
    - [NPA Threshold mockito](#npa-threshold-mockito)
    - [COA Threshold java-jwt](#coa-threshold-java-jwt)
    - [COA Threshold gson](#coa-threshold-gson)
    - [COA Threshold spring-kafka](#coa-threshold-spring-kafka)
    - [COA Threshold mockito](#coa-threshold-mockito)
    - [CDA Threshold java-jwt](#cda-threshold-java-jwt)
    - [CDA Threshold gson](#cda-threshold-gson)
    - [CDA Threshold spring-kafka](#cda-threshold-spring-kafka)
    - [CDA Threshold mockito](#cda-threshold-mockito)

### Cumulative measures

#### Averages java-jwt
<div align="center"><img src="./cumulative/average-measures-java-jwt-1.svg"></div>
<div align="center"><img src="./cumulative/average-measures-java-jwt-2.svg"></div>

#### Averages gson
<div align="center"><img src="./cumulative/average-measures-gson-1.svg"></div>
<div align="center"><img src="./cumulative/average-measures-gson-2.svg"></div>

#### Averages spring-kafka
<div align="center"><img src="./cumulative/average-measures-spring-kafka-1.svg"></div>
<div align="center"><img src="./cumulative/average-measures-spring-kafka-2.svg"></div>

#### Averages mockito
<div align="center"><img src="./cumulative/average-measures-mockito-1.svg"></div>
<div align="center"><img src="./cumulative/average-measures-mockito-2.svg"></div>

#### Maximums java-jwt
<div align="center"><img src="./cumulative/maximum-measures-java-jwt-1.svg"></div>
<div align="center"><img src="./cumulative/maximum-measures-java-jwt-2.svg"></div>

#### Maximums gson
<div align="center"><img src="./cumulative/maximum-measures-gson-1.svg"></div>
<div align="center"><img src="./cumulative/maximum-measures-gson-2.svg"></div>

#### Maximums spring-kafka
<div align="center"><img src="./cumulative/maximum-measures-spring-kafka-1.svg"></div>
<div align="center"><img src="./cumulative/maximum-measures-spring-kafka-2.svg"></div>

#### Maximums mockito
<div align="center"><img src="./cumulative/maximum-measures-mockito-1.svg"></div>
<div align="center"><img src="./cumulative/maximum-measures-mockito-2.svg"></div>

### Thresholds

| Metrics | Thresholds Found | Source | Threshold Chosen | Notes |
| --- | --- | --- | --- | --- |
| ABC | 60 | [Link 1](https://tenpercentnotcrap.wordpress.com/2013/01/14/groovy-code-metrics-abc/),</br>[Link 2](https://jakescruggs.blogspot.com/2008/08/whats-good-flog-score.html) | 60 | The threshold found comes from the Sonar ABC Plugin for Java code. |
| WMC | 34 | [Link 1](http://www.llp.dcc.ufmg.br/Publications/Art2015/softeng_2015_3_10_55070.pdf) | 34 | The threshold found comes from a recent paper. |
| NPM | 40 | [Link 1](https://it.booksc.org/book/13623664/efc340) | 40 | The threshold found comes from a recent paper. |
| NPA | 10 | [Link 1](https://it.booksc.org/book/13623664/efc340) | 10 | The threshold found was too high for the repositories. |
| COA | - | - | 1 | No threshold found. The worst value possible was taken as threshold. |
| CDA | - | - | 1 | No threshold found. The worst value possible was taken as threshold. |

#### ABC Threshold java-jwt
<div align="center"><img src="./thresholds/threshold-measures-abc-java-jwt.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-abc-java-jwt.svg"></div>

#### ABC Threshold gson
<div align="center"><img src="./thresholds/threshold-measures-abc-gson.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-abc-gson.svg"></div>

#### ABC Threshold spring-kafka
<div align="center"><img src="./thresholds/threshold-measures-abc-spring-kafka.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-abc-spring-kafka.svg"></div>

#### ABC Threshold mockito
<div align="center"><img src="./thresholds/threshold-measures-abc-mockito.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-abc-mockito.svg"></div>

#### WMC Threshold java-jwt
<div align="center"><img src="./thresholds/threshold-measures-wmc-java-jwt.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-wmc-java-jwt.svg"></div>

#### WMC Threshold gson
<div align="center"><img src="./thresholds/threshold-measures-wmc-gson.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-wmc-gson.svg"></div>

#### WMC Threshold spring-kafka
<div align="center"><img src="./thresholds/threshold-measures-wmc-spring-kafka.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-wmc-spring-kafka.svg"></div>

#### WMC Threshold mockito
<div align="center"><img src="./thresholds/threshold-measures-wmc-mockito.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-wmc-mockito.svg"></div>

#### NPM Threshold java-jwt
<div align="center"><img src="./thresholds/threshold-measures-npm-java-jwt.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-npm-java-jwt.svg"></div>

#### NPM Threshold gson
<div align="center"><img src="./thresholds/threshold-measures-npm-gson.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-npm-gson.svg"></div>

#### NPM Threshold spring-kafka
<div align="center"><img src="./thresholds/threshold-measures-npm-spring-kafka.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-npm-spring-kafka.svg"></div>

#### NPM Threshold mockito
<div align="center"><img src="./thresholds/threshold-measures-npm-mockito.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-npm-mockito.svg"></div>

#### NPA Threshold java-jwt
<div align="center"><img src="./thresholds/threshold-measures-npa-java-jwt.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-npa-java-jwt.svg"></div>

#### NPA Threshold gson
<div align="center"><img src="./thresholds/threshold-measures-npa-gson.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-npa-gson.svg"></div>

#### NPA Threshold spring-kafka
<div align="center"><img src="./thresholds/threshold-measures-npa-spring-kafka.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-npa-spring-kafka.svg"></div>

#### NPA Threshold mockito
<div align="center"><img src="./thresholds/threshold-measures-npa-mockito.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-npa-mockito.svg"></div>

#### COA Threshold java-jwt
<div align="center"><img src="./thresholds/threshold-measures-coa-java-jwt.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-coa-java-jwt.svg"></div>

#### COA Threshold gson
<div align="center"><img src="./thresholds/threshold-measures-coa-gson.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-coa-gson.svg"></div>

#### COA Threshold spring-kafka
<div align="center"><img src="./thresholds/threshold-measures-coa-spring-kafka.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-coa-spring-kafka.svg"></div>

#### COA Threshold mockito
<div align="center"><img src="./thresholds/threshold-measures-coa-mockito.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-coa-mockito.svg"></div>

#### CDA Threshold java-jwt
<div align="center"><img src="./thresholds/threshold-measures-cda-java-jwt.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-cda-java-jwt.svg"></div>

#### CDA Threshold gson
<div align="center"><img src="./thresholds/threshold-measures-cda-gson.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-cda-gson.svg"></div>

#### CDA Threshold spring-kafka
<div align="center"><img src="./thresholds/threshold-measures-cda-spring-kafka.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-cda-spring-kafka.svg"></div>

#### CDA Threshold mockito
<div align="center"><img src="./thresholds/threshold-measures-cda-mockito.svg"></div>
<div align="center"><img src="./thresholds/threshold-percentages-cda-mockito.svg"></div>