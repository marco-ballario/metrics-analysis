# Time Analysis

## Repositories
| Name | Last Version | Files | Source |
| --- | --- | --- | --- |
| [spring-kafka](https://github.com/spring-projects/spring-kafka) | v2.9.0 | 502 | [Maven Central](https://mvnrepository.com/artifact/org.springframework.kafka/spring-kafka) |
| [gson](https://github.com/google/gson) | gson-parent-2.9.1 | 218 | [Maven Central](https://mvnrepository.com/artifact/com.google.code.gson/gson) |
| [java-jwt](https://github.com/auth0/java-jwt) | 4.0.0 | 75 | [Maven Central](https://mvnrepository.com/artifact/com.auth0/java-jwt) |

## Graphs
- [Cumulative measures](#cumulative-measures)
    - [Averages java-jwt](#averages-java-jwt)
    - [Averages gson](#averages-gson)
    - [Averages spring-kafka](#averages-spring-kafka)
    - [Maximums java-jwt](#maximums-java-jwt)
    - [Maximums gson](#maximums-gson)
    - [Maximums spring-kafka](#maximums-spring-kafka)
- [Thresholds](#thresholds)
    - [ABC Threshold java-jwt](#abc-threshold-java-jwt)
    - [ABC Threshold gson](#abc-threshold-gson)
    - [ABC Threshold spring-kafka](#abc-threshold-spring-kafka)
    - [WMC Threshold java-jwt](#wmc-threshold-java-jwt)
    - [WMC Threshold gson](#wmc-threshold-gson)
    - [WMC Threshold spring-kafka](#wmc-threshold-spring-kafka)
    - [NPM Threshold java-jwt](#npm-threshold-java-jwt)
    - [NPM Threshold gson](#npm-threshold-gson)
    - [NPM Threshold spring-kafka](#npm-threshold-spring-kafka)
    - [NPA Threshold java-jwt](#npa-threshold-java-jwt)
    - [NPA Threshold gson](#npa-threshold-gson)
    - [NPA Threshold spring-kafka](#npa-threshold-spring-kafka)
    - [COA Threshold java-jwt](#coa-threshold-java-jwt)
    - [COA Threshold gson](#coa-threshold-gson)
    - [COA Threshold spring-kafka](#coa-threshold-spring-kafka)
    - [CDA Threshold java-jwt](#cda-threshold-java-jwt)
    - [CDA Threshold gson](#cda-threshold-gson)
    - [CDA Threshold spring-kafka](#cda-threshold-spring-kafka)

### Cumulative measures

#### Averages java-jwt
<div align="center"><img src="./cumulative/average-measures-java-jwt-1.png"></div>
<div align="center"><img src="./cumulative/average-measures-java-jwt-2.png"></div>

#### Averages gson
<div align="center"><img src="./cumulative/average-measures-gson-1.png"></div>
<div align="center"><img src="./cumulative/average-measures-gson-2.png"></div>

#### Averages spring-kafka
<div align="center"><img src="./cumulative/average-measures-spring-kafka-1.png"></div>
<div align="center"><img src="./cumulative/average-measures-spring-kafka-2.png"></div>

#### Maximums java-jwt
<div align="center"><img src="./cumulative/maximum-measures-java-jwt-1.png"></div>
<div align="center"><img src="./cumulative/maximum-measures-java-jwt-2.png"></div>

#### Maximums gson
<div align="center"><img src="./cumulative/maximum-measures-gson-1.png"></div>
<div align="center"><img src="./cumulative/maximum-measures-gson-2.png"></div>

#### Maximums spring-kafka
<div align="center"><img src="./cumulative/maximum-measures-spring-kafka-1.png"></div>
<div align="center"><img src="./cumulative/maximum-measures-spring-kafka-2.png"></div>

### Thresholds

| Metrics | Thresholds Found | Source | Threshold Chosen | Notes |
| --- | --- | --- | --- | --- |
| ABC | 60 | [Link 1](https://tenpercentnotcrap.wordpress.com/2013/01/14/groovy-code-metrics-abc/),</br>[Link 2](https://jakescruggs.blogspot.com/2008/08/whats-good-flog-score.html) | 60 | The threshold found comes from the Sonar ABC Plugin for Java code. |
| WMC | 34 | [Link 1](http://www.llp.dcc.ufmg.br/Publications/Art2015/softeng_2015_3_10_55070.pdf) | 34 | The threshold found comes from a recent paper. |
| NPM | 40 | [Link 1](https://it.booksc.org/book/13623664/efc340) | 40 | The threshold found comes from a recent paper. |
| NPA | 10 | [Link 1](https://it.booksc.org/book/13623664/efc340) | 0 | The threshold found was too high for the repositories. |
| COA | - | - | 1 | No threshold found. The worst value possible was taken as threshold. |
| CDA | - | - | 1 | No threshold found. The worst value possible was taken as threshold. |

#### ABC Threshold java-jwt
<div align="center"><img src="./thresholds/threshold-measures-abc-java-jwt.png"></div>
<div align="center"><img src="./thresholds/threshold-percentages-abc-java-jwt.png"></div>

#### ABC Threshold gson
<div align="center"><img src="./thresholds/threshold-measures-abc-gson.png"></div>
<div align="center"><img src="./thresholds/threshold-percentages-abc-gson.png"></div>

#### ABC Threshold spring-kafka
<div align="center"><img src="./thresholds/threshold-measures-abc-spring-kafka.png"></div>
<div align="center"><img src="./thresholds/threshold-percentages-abc-spring-kafka.png"></div>

#### WMC Threshold java-jwt
<div align="center"><img src="./thresholds/threshold-measures-wmc-java-jwt.png"></div>
<div align="center"><img src="./thresholds/threshold-percentages-wmc-java-jwt.png"></div>

#### WMC Threshold gson
<div align="center"><img src="./thresholds/threshold-measures-wmc-gson.png"></div>
<div align="center"><img src="./thresholds/threshold-percentages-wmc-gson.png"></div>

#### WMC Threshold spring-kafka
<div align="center"><img src="./thresholds/threshold-measures-wmc-spring-kafka.png"></div>
<div align="center"><img src="./thresholds/threshold-percentages-wmc-spring-kafka.png"></div>

#### NPM Threshold java-jwt
<div align="center"><img src="./thresholds/threshold-measures-npm-java-jwt.png"></div>
<div align="center"><img src="./thresholds/threshold-percentages-npm-java-jwt.png"></div>

#### NPM Threshold gson
<div align="center"><img src="./thresholds/threshold-measures-npm-gson.png"></div>
<div align="center"><img src="./thresholds/threshold-percentages-npm-gson.png"></div>

#### NPM Threshold spring-kafka
<div align="center"><img src="./thresholds/threshold-measures-npm-spring-kafka.png"></div>
<div align="center"><img src="./thresholds/threshold-percentages-npm-spring-kafka.png"></div>

#### NPA Threshold java-jwt
<div align="center"><img src="./thresholds/threshold-measures-npa-java-jwt.png"></div>
<div align="center"><img src="./thresholds/threshold-percentages-npa-java-jwt.png"></div>

#### NPA Threshold gson
<div align="center"><img src="./thresholds/threshold-measures-npa-gson.png"></div>
<div align="center"><img src="./thresholds/threshold-percentages-npa-gson.png"></div>

#### NPA Threshold spring-kafka
<div align="center"><img src="./thresholds/threshold-measures-npa-spring-kafka.png"></div>
<div align="center"><img src="./thresholds/threshold-percentages-npa-spring-kafka.png"></div>

#### COA Threshold java-jwt
<div align="center"><img src="./thresholds/threshold-measures-coa-java-jwt.png"></div>
<div align="center"><img src="./thresholds/threshold-percentages-coa-java-jwt.png"></div>

#### COA Threshold gson
<div align="center"><img src="./thresholds/threshold-measures-coa-gson.png"></div>
<div align="center"><img src="./thresholds/threshold-percentages-coa-gson.png"></div>

#### COA Threshold spring-kafka
<div align="center"><img src="./thresholds/threshold-measures-coa-spring-kafka.png"></div>
<div align="center"><img src="./thresholds/threshold-percentages-coa-spring-kafka.png"></div>

#### CDA Threshold java-jwt
<div align="center"><img src="./thresholds/threshold-measures-cda-java-jwt.png"></div>
<div align="center"><img src="./thresholds/threshold-percentages-cda-java-jwt.png"></div>

#### CDA Threshold gson
<div align="center"><img src="./thresholds/threshold-measures-cda-gson.png"></div>
<div align="center"><img src="./thresholds/threshold-percentages-cda-gson.png"></div>

#### CDA Threshold spring-kafka
<div align="center"><img src="./thresholds/threshold-measures-cda-spring-kafka.png"></div>
<div align="center"><img src="./thresholds/threshold-percentages-cda-spring-kafka.png"></div>
